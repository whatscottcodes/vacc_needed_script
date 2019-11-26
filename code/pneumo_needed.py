import argparse
import datetime
from paceutils import Quality

db_filepath = "V:\\Databases\\PaceDashboard.db"


def pneumo_needed_df(remove_refused=False):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    params = (today, today)

    quality = Quality(db_filepath)

    pneumo23_only = quality.need_pneumo_23_only(params)
    pneumo23_only["vacc_needed"] = "Pneumococcal 23"

    pcv13_only = quality.need_pcv_13_only(params)
    pcv13_only["vacc_needed"] = "PCV 13"

    both = quality.need_both_pneumo_vaccs(params)
    both["vacc_needed"] = "Both"

    need_vacc = pneumo23_only.append(pcv13_only).append(both)

    if remove_refused:
        refused = quality.refused_pneumo_vacc_list(params)["member_id"].unique()
        need_vacc = need_vacc[-need_vacc.member_id.isin(refused)].copy()

    need_vacc.to_csv(f".\\output\\pneumo_needed_{today}.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--remove_refused",
        default=False,
        help="Do we need to remove the ppts who have refused the vaccination in the past?",
    )

    arguments = parser.parse_args()

    pneumo_needed_df(**vars(arguments))
