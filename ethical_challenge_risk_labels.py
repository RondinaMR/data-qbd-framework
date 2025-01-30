from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor
from matplotlib import colors
from utilities import hex_to_rgb, rgb_to_hex, interpolate_color

def create_labels(dataset_name, dq_risk, db_risk, dd_risk, min_color, max_color):
    if db_risk is None:
        ethical_challenges = {
            "1_inconclusive_evidence": {
                "risk": dq_risk,
                "dim": 1,
                "line1": "Inconclusive",
                "line2": "evidence"
            },
            "2_inscrutable_evidence": {
                "risk": dq_risk + dd_risk,
                "dim": 2,
                "line1": "Inscrutable",
                "line2": "evidence"
            },
            "3_misguided_evidence": {
                "risk": dd_risk,
                "dim": 1,
                "line1": "Misguided",
                "line2": "evidence"
            },
            "4_unfair_outcomes": {
                "risk": dq_risk,
                "dim": 1,
                "line1": "Unfair",
                "line2": "outcomes"
            },
            "5_transformative_effects": {
                "risk": 0,
                "dim": 1,
                "line1": "Transformative",
                "line2": "effects (N/A)"
            },
            "6_traceability": {
                "risk": dq_risk + dd_risk,
                "dim": 2,
                "line1": "Traceability",
                "line2": ""
            },
        }
    else:
        ethical_challenges = {
            "1_inconclusive_evidence": {
                "risk": dq_risk,
                "dim": 1,
                "line1": "Inconclusive",
                "line2": "evidence"
            },
            "2_inscrutable_evidence": {
                "risk": dq_risk + dd_risk,
                "dim": 2,
                "line1": "Inscrutable",
                "line2": "evidence"
            },
            "3_misguided_evidence": {
                "risk": dd_risk,
                "dim": 1,
                "line1": "Misguided",
                "line2": "evidence"
            },
            "4_unfair_outcomes": {
                "risk": dq_risk + db_risk,
                "dim": 2,
                "line1": "Unfair",
                "line2": "outcomes"
            },
            "5_transformative_effects": {
                "risk": db_risk,
                "dim": 1,
                "line1": "Transformative",
                "line2": "effects"
            },
            "6_traceability": {
                "risk": dq_risk + db_risk + dd_risk,
                "dim": 3,
                "line1": "Traceability",
                "line2": ""
            },
        }
    
    font_properties = {
        "fontSize": 40,
        "fontName": "Courier",
        "fillColor": 'black'
    }

    for ethical_challenge in ethical_challenges:
        ratio = ethical_challenges[ethical_challenge]["risk"] / ethical_challenges[ethical_challenge]["dim"]
        print(dataset_name, ethical_challenge, f'{ratio*100:.2f}%')
        d = Drawing(400, 400)
        d.add(Rect(0, 0, 400, 400, fillColor=HexColor(f"#{interpolate_color(min_color, max_color, ratio)}")))
        d.add(Rect(375, 0, 25, 400, fillColor='white'))
        d.add(Rect(375, 0, 25, ratio * 400, fillColor='darkred'))
        d.add(String(18, 250, ethical_challenges[ethical_challenge]["line1"], fontSize=font_properties["fontSize"],
                     fontName=font_properties["fontName"], fillColor=font_properties["fillColor"]))
        if ethical_challenges[ethical_challenge]["line2"] != "":
            d.add(String(18, 150, ethical_challenges[ethical_challenge]["line2"], fontSize=font_properties["fontSize"],
                         fontName=font_properties["fontName"], fillColor=font_properties["fillColor"]))

        renderPDF.drawToFile(d, f'analysis/images/labels/{dataset_name.replace(" ", "")}_label_{ethical_challenge}.pdf',
                             f'{dataset_name}_label_{ethical_challenge}')
    return


def compute_ethical_challenge_risks_labels(dq_df, db_df, dd_df, dataset_names, dataset_dict, max_color, min_color):
    # Computation of the data quality risks sum
    dq_df_cols = ["Acc-I-4", "Com-I-1-DevA", "Com-I-5", "Con-I-2-DevB", "Con-I-3-DevC", "Con-I-4-DevD"]
    dq_df["risks_sum"] = dq_df[dq_df_cols].apply(
        lambda row: row["Acc-I-4"] + (1 - row["Com-I-1-DevA"]) + (1 - row["Com-I-5"]) + (1 - row["Con-I-2-DevB"]) + row[
            "Con-I-3-DevC"] + (1 - row["Con-I-4-DevD"]), axis=1)
    # Data quality risks ratio (sum divided by the maximum risk possible)
    dq_df["risk_ratio"] = dq_df["risks_sum"].apply(lambda row: row / 6)
    print("Data Quality\n", dq_df)

    # Computation of the data balance risks sum
    # Group by "Dataset" and compute sum for each group
    db_aggregate_df = db_df.groupby('Dataset').agg(
        {'Gini': lambda x: (1 - x).sum(), 'Shannon': lambda x: (1 - x).sum(), 'Simpson': lambda x: (1 - x).sum(),
        'I.I.R.': lambda x: (1 - x).sum(), 'Feature': 'count'})
    # Calculate "risk_ratio"
    db_aggregate_df['simpson_risk_ratio'] = db_aggregate_df['Simpson'] / db_aggregate_df['Feature']
    print("Data Balance\n", db_aggregate_df)

    # Computation of the data documentation risks sum
    # Exclude "Overall Presence Average" metric
    dd_aggregate_df = dd_df[dd_df["Metric"] != "Overall Presence Average"]
    # Group by "Dataset" and compute sum for each group
    dd_aggregate_df = dd_aggregate_df.groupby('Dataset').agg({'Value': lambda x: (1 - x).sum()})
    # Calculate "risk_ratio"
    dd_aggregate_df['risk_ratio'] = dd_aggregate_df['Value'] / 6
    print("Data Documentation\n", dd_aggregate_df)

    for dataset in dataset_names:
        if dataset in ["MovieLensMovies", "MovieLensRatings"]:
            continue
        dq_risk = dq_df.at[dataset, 'risk_ratio']
        try:
            db_risk = db_aggregate_df.at[dataset, 'simpson_risk_ratio']
        except KeyError:
            db_risk = None
        dd_risk = dd_aggregate_df.at[dataset, 'risk_ratio']
        create_labels(dataset_dict[dataset], dq_risk, db_risk, dd_risk, max_color, min_color)
    return

