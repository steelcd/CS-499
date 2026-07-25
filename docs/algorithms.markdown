---
layout: default
title: Algorithms and Data Structures
permalink: /algorithms/
---
{% include nav.html %}

## Algorithms and Data Structures
[Github Project Link](https://github.com/steelcd/CS-499/tree/module4-algorithms){:target="_blank"}

For this enhancement, I focused on improving how the AAC Rescue application identifies rescue animal candidates. The original dashboard used hardcoded filters for Water Rescue, Mountain or Wilderness Rescue, and Disaster or Individual Tracking. These filters worked for the original project, but they only returned exact matches. If an animal missed one requirement, it was excluded from the results, even if it matched several other useful criteria.

I replaced the fixed filters with a profile-driven scoring algorithm. Rescue profiles are stored in MongoDB and include eligibility requirements, scoring rules, weights, breed lists, and age ranges. The Node/Express API loads the selected rescue profile, applies the eligibility rules, scores each animal against the weighted criteria, and returns a ranked list of candidates. This allows the rescue profiles to be updated without changing the application code.

This enhancement also changed how the Dash dashboard gets its data. The original dashboard used PyMongo to query MongoDB directly. I removed that direct database connection and updated the Dash app so it requests scored candidate results from the Node/Express API. This keeps the scoring logic in one place and allows the dashboard to focus on displaying the ranked results and score breakdown.

The main data structures used in this enhancement are MongoDB documents, JavaScript objects, arrays, and sorted lists. Each rescue profile is stored as a document with an array of scoring rules. The API processes those rules against arrays of eligible animal records, calculates a score for each animal, and sorts the results before returning them to the dashboard. This improves the original artifact by turning static filters into a more flexible ranking process that better supports rescue candidate selection.

## Screenshots

### Rescue Profile Seed Data

![Rescue scoring profile in MongoDB]({{ "/assets/images/rescue_scoring_profile.png" | relative_url }})

### Node.js API Result

![Scored candidate API result]({{ "/assets/images/postman_api_result.png" | relative_url }})

### Dash App Filter Result

![Dash App updated to return scoring result]({{ "/assets/images/updated_dashboard.png" | relative_url }})
