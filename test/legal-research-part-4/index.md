+++
title =  "Conduct Legal Research with AI: Part 4"
date = "2022-05-19T22:30:32.169Z"
description = "Importing case variables and established relationships to the graph."
author = "Justin Napolitano"
image = "post-image.jpeg"
thumbnail = "post-image.jpeg"
featured = "post-image.jpeg"
categories = ['Legal Research', 'Data Wrangling', 'Graph Database', 'Automation']
tags = ['python','legal', 'json', 'scotus', 'automation']
images = ['featured-justices.jpeg']
series = ['Legal Research with AI']
+++

# Conduct Legal Research with AI Part 4


This is the fourth post in a series documenting the process of building an ml pipeline used to train models to predict the outcomes of Supreme Court cases.  

You can find the others at:

* Part 1: [blog.jnapolitano.io/neo4j_integration/](https://blog.jnapolitano.io/neo4j_integration/)
* Part 2: [blog.jnapolitano.io/constitution_to_neo/](https://blog.jnapolitano.io/constitution_to_neo/)
* Part 3: [blog.jnapolitano.io/ai-proof-of-concept/](https://blog.jnapolitano.io/ai-proof-of-concept/)

## Modeling the Supreme Court

Thankfully, much of the ground work has been done by contributors to [The Washington University of St. Louis Law School Supreme Court Database](http://scdb.wustl.edu/documentation.php)

Unfortunately, The Supreme Court Database is limited in its scope. My approach extends their work by  creating a graph database.  

I have chosen to model the data in a graph database with a Person, Object, Event, Location (POLE) schema.  This will permit me to relate cases, justices, subjects, objects, ideas, and events to one another to train ML models to automate much of the legal research pipeline.  

The models could be ported to work with any body of jurisprudence.  

## The Case Class

In this post, I publish only the Case schema that will be used to relate cases to other objects for a machine learning algorithm to predict the outcomes, subjects, and legal provisions of court cases.  

A detailed report documenting each variable will be produced in the future when I publish the database.  For the time being, the Case class below should suitably demonstrate the foundation of the database.  

I will continue to publish the remaining classes as they are completed.  

```python
class Case(StructuredNode):
    #####Media########
    pdf = StringProperty(unique_index=True, required=True) 

    #### Identification Variables####
    uid = UniqueIdProperty()

    group = StringProperty(unique_index=True, required=True)

    loc_title = StringProperty(unique_index=True, required=True)

    url = StringProperty(unique_index=True, required=True)
    
    shelf_id = StringProperty()

    usCite = StringProperty(unique_index=True, required=True)
    
    
    caseId = StringProperty(unique_index=True, required=True)
   
    caseName = StringProperty(unique_index=True, required=True)
    
    scdb_docket_id = StringProperty(unique_index=True, required=True)
    
    scdb_vote_id = StringProperty(unique_index=True, required=True)
    
    scdb_issues_id = StringProperty(unique_index=True, required=True)
    
    supCite = StringProperty(unique_index=True, required=True)
    
    lawEdCite = StringProperty(unique_index=True, required=True)
    
    lexisCite = StringProperty(unique_index=True, required=True)
    
    dockNumb = StringProperty(unique_index=True, required=True)

    ######background Variables########
    name = StringProperty(unique_index=True, required=True)
    petitioner = Relationship('Petitioner', 'IS_PETITIONER')
    petitionState = Relationship('State', 'IS_PETITIONER')

    respondent = Relationship('Respondent', 'IS_RESPONDENT')
    respondentState = Relationship('State', 'IS_RESPONDENT')

    jurisdiction = Relationship('Jurisdiction', 'JURISDICTION')
    
    adminAction = Relationship('Admin', 'ACTION')

    threeJudgeFdc = BooleanProperty()

    origin = Relationship('USCOURT', 'ORIGIN')

    origin_state = Relationship('State', 'ORIGIN')

    source = Relationship('Source', 'SOURCE')

    source_state = Relationship('State', 'SOURCE')

    lc_disagreement = BooleanProperty()

    certReason = Relationship('CertReason', 'REASON')

    lc_disposition = Relationship('Disposition', 'LC_DISPOSITION')

    lc_direction = Relationship('Direction', 'LC_DIRECTION')

    #####3 Chronological #####

    # From Spaethe
    dateArgument = DateProperty()
    dateDecision = DateProperty()
    dateReargue = DateProperty()

    # From LOC
    date = StringProperty(unique_index=True, required=True)
    dates = StringProperty(unique_index=True, required=True)
    
    term = Relationship('Term', 'TERM_OF')
    natCourt = Relationship('Natcourt','NAT_COURT')

    chief = Relationship('Justice', 'IS_CHIEF')

    ######Substantive#####

    subject = StringProperty(unique_index=True, required=True)

    decisionDirection = Relationship('Direction', 'SUP_COURT_MAJORITY_DIRECTION')
    
    decisionDirectionDissent = Relationship('Direction', 'SUP_COURT_DISSENT_DIRECTION')
    
    spaethIssue = Relationship('SpaethIssue', 'IS_SPAETH_ISSUE')
    
    spaethIssueArea = Relationship('SpaethIssueArea', 'IS_SPAETH_ISSUE_AREA')

    subject_relationship = Relationship("Subject", "IS_CASE_OF")
    
    article = Relationship("Case", 'IS_ARTICLE_OF')
    
    clause = Relationship("Clause", 'IS_CLAUSE_OF')
    
    section = Relationship("Section", 'IS_SECTION_OF')
    
    sub_clause = Relationship("Subclause", 'IS_SUB_CLAUSE_OF')
    
    major_case_topic = Relationship('Subject', 'IS_MAJOR_TOPIC')

    authority = Relationship('Authority', 'IS_AUTHORITY')

    legalProvision = Relationship('legalProvision', 'IS_PROVISION')
    
    lawType = Relationship('lawType', 'lawType')

    law = Relationship('Law', 'SUPPORTING_LAW')

   
    ######Outcome Variables#####

    decisionType = Relationship('DecisionType', 'IS_DECISION_TYPE')

    declarationUnconstitutional = Relationship('Constitutional','UNCONSTITUTIONAL')
    
    delcarationConstitutional = Relationship('Constitutional', "CONSTITUTIONAL")

    disposition = Relationship('Disposition', 'IS_DISPOSITION')

    winningParty = Relationship('Party', 'IS_WINNER')
    FormalAlterationOfPrecedent = BooleanProperty()
    
    alteredPrecedent = Relationship("Case", 'Altered_Precedent')
    

    ## Voting and Opinion Variables
    # will account for all types of votes a node for each outcome
    vote = Relationship('Vote', 'OUTCOME')
    
    majOpinWriter = Relationship('Justice', 'WROTE_MAJORITY_OPINION')
    
    majOpinWriter = Relationship('Justice', "ASSIGNED_MAJORITY_OPINION")

    affirmative_vote = Relationship('Justice', "AFFIRMATE_VOTE")
    
    negative_vote = Relationship('Justice', "NEGATIVE_VOTE")

    conservative_vote = Relationship('Justice', 'CONSERVATIVE')
    liberal_vote = Relationship('Justice', "LIBERAL")

    majority_vote = Relationship('Justice', 'MAJORITY_VOTE')

    miniority_vote = Relationship('Justice','MINORITY_VOTE')

    wrote_an_opinion = Relationship('Justice', 'WROTE_AN_OPINION')

    co_authored_opinion = Relationship('Justice', "COAUTHORED_OPINION")

    agreed_with_concurrence = Relationship('Justice', 'AGREED_WITH_CONCURRENCE')

    agreed_with_dissent = Relationship('Justice', 'AGREED_WITH_CONCURRENCE')
```