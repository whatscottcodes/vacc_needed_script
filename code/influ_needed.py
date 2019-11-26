import datetime
from paceutils import Quality

db_filepath = "V:\\Databases\\PaceDashboard.db"


def influ_needed_df(params=None):
    if params is None:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        params = (today, today)

    quality = Quality(db_filepath)

    need_vacc = quality.need_influenza_vacc_df(params)
    refused = quality.refused_influ_vacc_df(params)

    need_vacc["status"] = "no record"
    refused["status"] = "refused"
    vacc_df = need_vacc.append(refused, sort=False)
    vacc_df.to_csv(f".\\output\\influ_needed_or_refused_{today}.csv", index=False)


if __name__ == "__main__":

    influ_needed_df()
