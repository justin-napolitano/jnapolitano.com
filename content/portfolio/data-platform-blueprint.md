+++
title = "Data Platform Blueprint"
date = 2024-07-18T10:30:00-04:00
description = "Designing a modular analytics platform on top of open-source tooling."
project_url = "https://github.com/justin-napolitano"
tools = ["dbt", "DuckDB", "Airflow", "Terraform"]
draft = false
+++

I scoped an end-to-end analytics platform that ingests CSV drops, stages them in object storage, models them with dbt, and ships curated marts into DuckDB for lightweight exploration. The infrastructure is defined in Terraform so new environments spin up quickly. The repo documents the architecture decisions, schema contracts, and alerting strategy.
