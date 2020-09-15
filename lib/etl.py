import pandas as pd


__all__ = ("get_acquisition_facts", "get_people")


def get_acquisition_facts(input_path="../static/input", output_path="../static/output"):
    acquisitions = pd.read_csv(f"{input_path}/cons_email_chapter_subscription.csv.gz")
    acquisitions = acquisitions[["cons_email_id", "chapter_id", "modified_dt"]]
    acquisitions = acquisitions.drop_duplicates(subset="cons_email_id")

    # If an email is not present in this table,
    # it is assumed to still be subscribed where chapter_id is 1
    acquisitions["chapter_id"] = acquisitions["chapter_id"].fillna(1)

    # We only care about subscription statuses where chapter_id is 1
    acquisitions = acquisitions[acquisitions["chapter_id"] == 1]

    # Aggregate acquisition facts
    acquisitions["acquisitions"] = 1
    acquisitions = acquisitions.rename(columns={"modified_dt": "acquisition_date"})
    acquisitions = acquisitions[["acquisition_date", "acquisitions"]]
    acquisitions["acquisition_date"] = pd.to_datetime(
        acquisitions["acquisition_date"], format="%a, %Y-%m-%d %H:%M:%S"
    )
    acquisitions["acquisition_date"] = acquisitions["acquisition_date"].dt.date
    acquisitions = acquisitions.groupby("acquisition_date")["acquisitions"].sum()

    print(acquisitions.sample(10))
    acquisitions.to_csv(f"{output_path}/task_2.csv")


def get_people(input_path="../static/input", output_path="../static/output"):
    people = pd.read_csv(f"{input_path}/cons.csv.gz", dtype={"source": "object"})
    people = people[["cons_id", "source", "create_dt", "modified_dt"]]

    emails = pd.read_csv(
        f"{input_path}/cons_email.csv.gz", dtype={"is_primary": "boolean"}
    )
    emails = emails[["cons_id", "cons_email_id", "is_primary", "email"]]
    emails = emails[emails["is_primary"] == 1]
    people = people.merge(emails, how="left", on="cons_id")

    acquisitions = pd.read_csv(
        f"{input_path}/cons_email_chapter_subscription.csv.gz",
        dtype={"isunsub": "boolean"},
    )
    acquisitions = acquisitions[["cons_email_id", "isunsub"]]
    people = people.merge(acquisitions, how="left", on="cons_email_id")

    people = people.rename(
        columns={
            "source": "code",
            "isunsub": "is_unsub",
            "create_dt": "created_dt",
            "modified_dt": "updated_dt",
        }
    )
    people["is_unsub"] = people["is_unsub"].fillna(False)
    people = people[["email", "code", "is_unsub", "created_dt", "updated_dt"]]
    people["created_dt"] = pd.to_datetime(
        people["created_dt"], format="%a, %Y-%m-%d %H:%M:%S"
    )
    people["updated_dt"] = pd.to_datetime(
        people["updated_dt"], format="%a, %Y-%m-%d %H:%M:%S"
    )

    print(people.sample(10))
    people.to_csv(f"{output_path}/task_1.csv", index=False)
