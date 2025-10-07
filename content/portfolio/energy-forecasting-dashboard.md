+++
title = "Energy Forecasting Dashboard"
date = 2024-05-03T14:00:00-04:00
description = "Forecasting regional energy demand with a lightweight visualization layer."
project_url = "https://jnapolitano.com/en/posts/european-gas-imports/"
tools = ["Python", "Prophet", "Observable"]
draft = false
+++

I prototyped a forecasting workflow that pairs Prophet models with an interactive dashboard. The pipeline runs inside Docker, publishes artifacts to GitHub Pages, and pushes summarized metrics into the site. Observable notebooks drive the visuals so stakeholders can tweak filters without touching the backend.
