"""
Reports Router — PDF and CSV report generation.
"""
import io
import csv
import datetime
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from database.models import Evaluation
from beanie import PydanticObjectId

router = APIRouter()


@router.get("/report/pdf/{evaluation_id}")
async def generate_pdf_report(evaluation_id: str):
    """Generate a PDF report for a stored evaluation."""
    evaluation = await Evaluation.get(PydanticObjectId(evaluation_id))
    if not evaluation:
        return {"error": "Evaluation not found"}

    result = evaluation.full_result or {}
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5 * inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("Title2", parent=styles["Title"], fontSize=16, spaceAfter=12)
    heading_style = ParagraphStyle("Heading", parent=styles["Heading2"], fontSize=12, spaceAfter=6)
    body_style = styles["BodyText"]

    elements = []

    # Title
    elements.append(Paragraph("LRES — Land Evaluation Report", title_style))
    elements.append(Paragraph(f"Generated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", body_style))
    elements.append(Spacer(1, 12))

    # Location
    loc = result.get("location", {})
    elements.append(Paragraph("Location", heading_style))
    elements.append(Paragraph(f"Coordinates: {evaluation.latitude}, {evaluation.longitude}", body_style))
    elements.append(Paragraph(f"State: {loc.get('state', 'N/A')} | District: {loc.get('district', 'N/A')}", body_style))
    elements.append(Paragraph(f"Region Type: {loc.get('region_type', 'N/A')}", body_style))
    elements.append(Spacer(1, 8))

    # Valuation
    preds = result.get("predictions", {})
    lr = preds.get("land_rate", {})
    elements.append(Paragraph("Land Valuation", heading_style))
    elements.append(Paragraph(f"Predicted Rate: ₹ {lr.get('predicted_rate_lakhs', 'N/A')} Lakhs per acre", body_style))
    elements.append(Paragraph(f"Best Use: {preds.get('land_use', {}).get('predicted_use', 'N/A')}", body_style))
    elements.append(Spacer(1, 8))

    # Soil
    soil = result.get("soil", {})
    elements.append(Paragraph("Soil Summary", heading_style))
    soil_data = [
        ["Property", "Value"],
        ["Soil Type", soil.get("soil_type", "N/A")],
        ["pH", str(soil.get("ph", "N/A"))],
        ["Organic Carbon", f"{soil.get('organic_carbon', 'N/A')}%"],
        ["Texture", soil.get("texture", "N/A")],
    ]
    table = Table(soil_data, colWidths=[2 * inch, 3 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d5016")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 8))

    # Crops
    crops = preds.get("crop_recommendations", {}).get("top_crops", [])
    if crops:
        elements.append(Paragraph("Crop Recommendations", heading_style))
        crop_data = [["Crop", "Suitability", "Season"]]
        for c in crops[:5]:
            crop_data.append([c["crop"], f"{c['suitability_pct']}%", c["season"]])
        table = Table(crop_data, colWidths=[1.5 * inch, 1.5 * inch, 2.5 * inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d5016")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 8))

    # Risk
    risk = preds.get("risk_analysis", {})
    elements.append(Paragraph("Risk Analysis", heading_style))
    elements.append(Paragraph(f"Risk Level: {risk.get('risk_level', 'N/A')} (Score: {risk.get('risk_score', 'N/A')})", body_style))
    for f in risk.get("risk_factors", []):
        elements.append(Paragraph(f"• {f}", body_style))
    elements.append(Spacer(1, 12))

    # Disclaimer
    elements.append(Paragraph("Disclaimer", heading_style))
    elements.append(Paragraph(
        "This report is generated for academic purposes using publicly available data and ML models. "
        "Actual land rates may vary. Consult local authorities for official valuations.",
        ParagraphStyle("Disclaimer", parent=body_style, fontSize=8, textColor=colors.grey),
    ))

    doc.build(elements)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=LRES_Report_{evaluation_id}.pdf"},
    )


@router.get("/report/csv/{evaluation_id}")
async def generate_csv_report(evaluation_id: str):
    """Generate a CSV export for a stored evaluation."""
    evaluation = await Evaluation.get(PydanticObjectId(evaluation_id))
    if not evaluation:
        return {"error": "Evaluation not found"}

    result = evaluation.full_result or {}
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    writer.writerow(["Field", "Value"])
    writer.writerow(["Latitude", evaluation.latitude])
    writer.writerow(["Longitude", evaluation.longitude])
    writer.writerow(["State", evaluation.state])
    writer.writerow(["District", evaluation.district])
    writer.writerow(["Region Type", evaluation.region_type])
    writer.writerow(["Soil Type", evaluation.soil_type])
    writer.writerow(["Soil pH", evaluation.soil_ph])
    writer.writerow(["Climate Zone", evaluation.climate_zone])
    writer.writerow(["Predicted Land Rate", evaluation.predicted_land_rate])
    writer.writerow(["Land Use", evaluation.land_use_prediction])
    writer.writerow(["Risk Level", evaluation.risk_level])
    writer.writerow(["Recommended Crops", ", ".join(evaluation.recommended_crops or [])])

    buffer.seek(0)
    return StreamingResponse(
        io.BytesIO(buffer.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=LRES_Report_{evaluation_id}.csv"},
    )


@router.get("/evaluations")
async def list_evaluations(limit: int = 20):
    """List recent evaluations from the database."""
    evaluations = await Evaluation.find_all().sort("-created_at").limit(limit).to_list()
    return [
        {
            "id": str(e.id),
            "lat": e.latitude,
            "lng": e.longitude,
            "state": e.state,
            "district": e.district,
            "predicted_rate": e.predicted_land_rate,
            "land_use": e.land_use_prediction,
            "risk_level": e.risk_level,
            "created_at": e.created_at.isoformat() if e.created_at else None,
        }
        for e in evaluations
    ]
