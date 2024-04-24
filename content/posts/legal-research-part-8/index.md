+++
title = "Conduct Legal Research with AI Part 8: Case Nodes Sample Data"
date = "2022-05-23T16:30:32.169Z"
description = "Merging Oyez and Library of Congress Data into a Comprehensive Data Set"
author = "Justin Napolitano"
image = "post-image.jpeg"
categories = ['Legal Research', 'Data Wrangling', 'Graph Database', 'Automation']
tags = ['python','legal', 'json', 'scotus', 'automation']
images = ['feature-image.png']
series = ['Legal Research with AI']
+++

## Introduction

The legal Research with AI Series is expanding quickly. This is the 9th post related to it in someway.  Building this pipeline and integrating multiple datasets into nodes is proving to be verbose.  

This post documents merging Oyez and Library of Congress of data structured json files that represent nodes and hierarchal relationships. 

## Main Function 
The plan for this program is to: 
* Read the prepared dataframe created in the [legal research part 7 post](https://blog.jnapolitano.io/posts/legal-research-part-7/)
* for each row of the df load a dictionary from the the libary of congress path and the oyez path
* Set keys on the Oyez dataset
* Write the updated Oyez dataset to file


Review the work below: 

``` Python
def main():

    # outpath fo the current file
    inpath = os.sep.join([os.getcwd(),"case_files.csv"])
    outpath = os.sep.join([os.getcwd(),"nodes"])
    
    #Create a df from the case_files.csv file
    master_df = pd.read_csv(inpath)
    for index, row in master_df.iterrows():
            
        oyez_dict = read_json(row["Path"])
        loc_dict = read_json(row['Path_1'])
        oyez_dict['loc_id'] = loc_dict['id']
        oyez_dict['loc_url'] = loc_dict['id']
        oyez_dict['simple_citation'] = loc_dict['loc_id']
        oyez_dict['shelf_id'] = loc_dict['shelf_id']
        oyez_dict['title'] = loc_dict['title']
        oyez_dict['issues'] = nodify_list(loc_dict['subject'],'issue')
        try:
            oyez_dict['major_topics'] = nodify_list(loc_dict['subject_major_case_topic'], 'major_topic')
        except:
            oyez_dict['major_topics'] = [""]
        oyez_dict['loc_pdf'] = loc_dict['resources'][0]['pdf']

        outfile = os.sep.join([outpath,oyez_dict['simple_citation']])
        outfile = outfile + ".json"

        with open(outfile, "w") as f: 
            json.dump(outpath,f)
```

## Helper Functions

### Read Json

read_json simply reads json into a dictionary with the json.loads method with a context manager.   

```Python

def read_json(file_path):
    with open(file_path) as f: 
        dict = json.load(f)
    return dict

```

### Nodify List

Some of the data in the Loc dataset is stored in lists.  I want them to be individual nodes in the final dataset.  To account for this, the nodify_list function returns a list of dictionaries containing keys that will be used to construct graph nodes.   I will most likely need to modify these as the graph schema expands with more data.  



```Python

    
def nodify_list(lst,node_name):
    return_list=[]
    for item in lst: 
        dict = {node_name: item}
        return_list.append(dict)
    return return_list
```


## The Complete Program 

``` python

#merging.python
from doctest import master
import os
import pandas as pd
from pprint import pprint
import json

def read_json(file_path):
    with open(file_path) as f: 
        dict = json.load(f)
    return dict

    
def nodify_list(lst,node_name):
    return_list=[]
    for item in lst: 
        dict = {node_name: item}
        return_list.append(dict)
    return return_list

def main():

    # outpath fo the current file
    inpath = os.sep.join([os.getcwd(),"case_files.csv"])
    outpath = os.sep.join([os.getcwd(),"nodes"])
    
    #Create a df from the case_files.csv file
    master_df = pd.read_csv(inpath)
    for index, row in master_df.iterrows():
            
        oyez_dict = read_json(row["Path"])
        loc_dict = read_json(row['Path_1'])
        oyez_dict['loc_id'] = loc_dict['id']
        oyez_dict['loc_url'] = loc_dict['id']
        oyez_dict['simple_citation'] = loc_dict['loc_id']
        oyez_dict['shelf_id'] = loc_dict['shelf_id']
        oyez_dict['title'] = loc_dict['title']
        oyez_dict['issues'] = nodify_list(loc_dict['subject'],'issue')
        try:
            oyez_dict['major_topics'] = nodify_list(loc_dict['subject_major_case_topic'], 'major_topic')
        except:
            oyez_dict['major_topics'] = [""]
        oyez_dict['loc_pdf'] = loc_dict['resources'][0]['pdf']

        outfile = os.sep.join([outpath,oyez_dict['simple_citation']])
        outfile = outfile + ".json"

        with open(outfile, "w") as f: 
            json.dump(oyez_dict,f, indent = 6)
        


    #pprint(oyez_dict)
if __name__ == "__main__":
    main()
```


## Sample Json Output


Below is a sample of what the program outputs.  It is a single case.


```json
{
      "decisions": [
            {
                  "href": "https://api.oyez.org/case_decision/case_decision/16396",
                  "votes": [
                        {
                              "ideology": 0,
                              "seniority": 1,
                              "opinion_type": "majority",
                              "member": {
                                    "href": "https://api.oyez.org/people/john_marshall",
                                    "ID": 15085,
                                    "last_name": "Marshall",
                                    "thumbnail": {
                                          "size": 53035,
                                          "href": "https://api.oyez.org/sites/default/files/images/people/john_marshall/john_marshall.thumb.png",
                                          "id": 32729,
                                          "mime": "image/png"
                                    },
                                    "length_of_service": 12570,
                                    "view_count": 0,
                                    "identifier": "john_marshall",
                                    "roles": [
                                          {
                                                "appointing_president": "John Adams",
                                                "href": "https://api.oyez.org/preson_role/scotus_justice/2729",
                                                "role_title": "Chief Justice of the United States",
                                                "type": "scotus_justice",
                                                "date_end": -4244119200,
                                                "id": 2729,
                                                "date_start": -5330167200,
                                                "institution_name": "Supreme Court of the United States"
                                          }
                                    ],
                                    "name": "John Marshall"
                              },
                              "href": "https://api.oyez.org/decision_vote/decision_vote/205605",
                              "vote": "majority",
                              "joining": null
                        },
                        {
                              "ideology": 0,
                              "seniority": 4,
                              "opinion_type": "none",
                              "member": {
                                    "href": "https://api.oyez.org/people/bushrod_washington",
                                    "ID": 15093,
                                    "last_name": "Washington",
                                    "thumbnail": {
                                          "size": 42759,
                                          "href": "https://api.oyez.org/sites/default/files/images/people/bushrod_washington/bushrod_washington.thumb.png",
                                          "id": 32698,
                                          "mime": "image/png"
                                    },
                                    "length_of_service": 11339,
                                    "view_count": 0,
                                    "identifier": "bushrod_washington",
                                    "roles": [
                                          {
                                                "appointing_president": "John Adams",
                                                "href": "https://api.oyez.org/preson_role/scotus_justice/2737",
                                                "role_title": "Associate Justice of the Supreme Court of the United States",
                                                "type": "scotus_justice",
                                                "date_end": -4421066400,
                                                "id": 2737,
                                                "date_start": -5400756000,
                                                "institution_name": "Supreme Court of the United States"
                                          }
                                    ],
                                    "name": "Bushrod Washington"
                              },
                              "href": "https://api.oyez.org/decision_vote/decision_vote/205606",
                              "vote": "majority",
                              "joining": [
                                    {
                                          "href": "https://api.oyez.org/people/john_marshall",
                                          "ID": 15085,
                                          "last_name": "Marshall",
                                          "thumbnail": {
                                                "size": 53035,
                                                "href": "https://api.oyez.org/sites/default/files/images/people/john_marshall/john_marshall.thumb.png",
                                                "id": 32729,
                                                "mime": "image/png"
                                          },
                                          "length_of_service": 12570,
                                          "view_count": 0,
                                          "identifier": "john_marshall",
                                          "roles": [
                                                {
                                                      "appointing_president": "John Adams",
                                                      "href": "https://api.oyez.org/preson_role/scotus_justice/2729",
                                                      "role_title": "Chief Justice of the United States",
                                                      "type": "scotus_justice",
                                                      "date_end": -4244119200,
                                                      "id": 2729,
                                                      "date_start": -5330167200,
                                                      "institution_name": "Supreme Court of the United States"
                                                }
                                          ],
                                          "name": "John Marshall"
                                    }
                              ]
                        },
                        {
                              "ideology": 0,
                              "seniority": 5,
                              "opinion_type": "concurrence",
                              "member": {
                                    "href": "https://api.oyez.org/people/william_johnson",
                                    "ID": 15059,
                                    "last_name": "Johnson",
                                    "thumbnail": {
                                          "size": 45940,
                                          "href": "https://api.oyez.org/sites/default/files/images/people/william_johnson/william_johnson.thumb.png",
                                          "id": 32779,
                                          "mime": "image/png"
                                    },
                                    "length_of_service": 11046,
                                    "view_count": 0,
                                    "identifier": "william_johnson",
                                    "roles": [
                                          {
                                                "appointing_president": "Thomas Jefferson",
                                                "href": "https://api.oyez.org/preson_role/scotus_justice/2703",
                                                "role_title": "Associate Justice of the Supreme Court of the United States",
                                                "type": "scotus_justice",
                                                "date_end": -4273149600,
                                                "id": 2703,
                                                "date_start": -5227524000,
                                                "institution_name": "Supreme Court of the United States"
                                          }
                                    ],
                                    "name": "William Johnson"
                              },
                              "href": "https://api.oyez.org/decision_vote/decision_vote/205607",
                              "vote": "majority",
                              "joining": [
                                    {
                                          "href": "https://api.oyez.org/people/john_marshall",
                                          "ID": 15085,
                                          "last_name": "Marshall",
                                          "thumbnail": {
                                                "size": 53035,
                                                "href": "https://api.oyez.org/sites/default/files/images/people/john_marshall/john_marshall.thumb.png",
                                                "id": 32729,
                                                "mime": "image/png"
                                          },
                                          "length_of_service": 12570,
                                          "view_count": 0,
                                          "identifier": "john_marshall",
                                          "roles": [
                                                {
                                                      "appointing_president": "John Adams",
                                                      "href": "https://api.oyez.org/preson_role/scotus_justice/2729",
                                                      "role_title": "Chief Justice of the United States",
                                                      "type": "scotus_justice",
                                                      "date_end": -4244119200,
                                                      "id": 2729,
                                                      "date_start": -5330167200,
                                                      "institution_name": "Supreme Court of the United States"
                                                }
                                          ],
                                          "name": "John Marshall"
                                    }
                              ]
                        },
                        {
                              "ideology": 0,
                              "seniority": 6,
                              "opinion_type": "none",
                              "member": {
                                    "href": "https://api.oyez.org/people/brockholst_livingston",
                                    "ID": 15111,
                                    "last_name": "Livingston",
                                    "thumbnail": {
                                          "size": 44786,
                                          "href": "https://api.oyez.org/sites/default/files/images/people/brockholst_livingston/brockholst_livingston.thumb.png",
                                          "id": 32714,
                                          "mime": "image/png"
                                    },
                                    "length_of_service": 5901,
                                    "view_count": 0,
                                    "identifier": "brockholst_livingston",
                                    "roles": [
                                          {
                                                "appointing_president": "Thomas Jefferson",
                                                "href": "https://api.oyez.org/preson_role/scotus_justice/2755",
                                                "role_title": "Associate Justice of the Supreme Court of the United States",
                                                "type": "scotus_justice",
                                                "date_end": -4632314400,
                                                "id": 2755,
                                                "date_start": -5142160800,
                                                "institution_name": "Supreme Court of the United States"
                                          }
                                    ],
                                    "name": "Henry Brockholst Livingston"
                              },
                              "href": "https://api.oyez.org/decision_vote/decision_vote/205608",
                              "vote": "majority",
                              "joining": [
                                    {
                                          "href": "https://api.oyez.org/people/john_marshall",
                                          "ID": 15085,
                                          "last_name": "Marshall",
                                          "thumbnail": {
                                                "size": 53035,
                                                "href": "https://api.oyez.org/sites/default/files/images/people/john_marshall/john_marshall.thumb.png",
                                                "id": 32729,
                                                "mime": "image/png"
                                          },
                                          "length_of_service": 12570,
                                          "view_count": 0,
                                          "identifier": "john_marshall",
                                          "roles": [
                                                {
                                                      "appointing_president": "John Adams",
                                                      "href": "https://api.oyez.org/preson_role/scotus_justice/2729",
                                                      "role_title": "Chief Justice of the United States",
                                                      "type": "scotus_justice",
                                                      "date_end": -4244119200,
                                                      "id": 2729,
                                                      "date_start": -5330167200,
                                                      "institution_name": "Supreme Court of the United States"
                                                }
                                          ],
                                          "name": "John Marshall"
                                    }
                              ]
                        },
                        {
                              "ideology": 0,
                              "seniority": 7,
                              "opinion_type": "none",
                              "member": {
                                    "href": "https://api.oyez.org/people/thomas_todd",
                                    "ID": 15039,
                                    "last_name": "Todd",
                                    "thumbnail": {
                                          "size": 41113,
                                          "href": "https://api.oyez.org/sites/default/files/images/people/thomas_todd/thomas_todd.thumb.png",
                                          "id": 32769,
                                          "mime": "image/png"
                                    },
                                    "length_of_service": 6854,
                                    "view_count": 0,
                                    "identifier": "thomas_todd",
                                    "roles": [
                                          {
                                                "appointing_president": "Thomas Jefferson",
                                                "href": "https://api.oyez.org/preson_role/scotus_justice/2683",
                                                "role_title": "Associate Justice of the Supreme Court of the United States",
                                                "type": "scotus_justice",
                                                "date_end": -4540989600,
                                                "id": 2683,
                                                "date_start": -5133175200,
                                                "institution_name": "Supreme Court of the United States"
                                          }
                                    ],
                                    "name": "Thomas Todd"
                              },
                              "href": "https://api.oyez.org/decision_vote/decision_vote/205609",
                              "vote": "majority",
                              "joining": [
                                    {
                                          "href": "https://api.oyez.org/people/john_marshall",
                                          "ID": 15085,
                                          "last_name": "Marshall",
                                          "thumbnail": {
                                                "size": 53035,
                                                "href": "https://api.oyez.org/sites/default/files/images/people/john_marshall/john_marshall.thumb.png",
                                                "id": 32729,
                                                "mime": "image/png"
                                          },
                                          "length_of_service": 12570,
                                          "view_count": 0,
                                          "identifier": "john_marshall",
                                          "roles": [
                                                {
                                                      "appointing_president": "John Adams",
                                                      "href": "https://api.oyez.org/preson_role/scotus_justice/2729",
                                                      "role_title": "Chief Justice of the United States",
                                                      "type": "scotus_justice",
                                                      "date_end": -4244119200,
                                                      "id": 2729,
                                                      "date_start": -5330167200,
                                                      "institution_name": "Supreme Court of the United States"
                                                }
                                          ],
                                          "name": "John Marshall"
                                    }
                              ]
                        },
                        {
                              "ideology": 0,
                              "seniority": 2,
                              "opinion_type": "none",
                              "member": {
                                    "href": "https://api.oyez.org/people/william_cushing",
                                    "ID": 15077,
                                    "last_name": "Cushing",
                                    "thumbnail": {
                                          "size": 52796,
                                          "href": "https://api.oyez.org/sites/default/files/images/people/william_cushing/william_cushing.thumb.png",
                                          "id": 32776,
                                          "mime": "image/png"
                                    },
                                    "length_of_service": 7527,
                                    "view_count": 0,
                                    "identifier": "william_cushing",
                                    "roles": [
                                          {
                                                "appointing_president": "George Washington",
                                                "href": "https://api.oyez.org/preson_role/scotus_justice/2721",
                                                "role_title": "Associate Justice of the Supreme Court of the United States",
                                                "type": "scotus_justice",
                                                "date_end": -5027076000,
                                                "id": 2721,
                                                "date_start": -5677408800,
                                                "institution_name": "Supreme Court of the United States"
                                          }
                                    ],
                                    "name": "William Cushing"
                              },
                              "href": "https://api.oyez.org/decision_vote/decision_vote/205610",
                              "vote": "none",
                              "joining": null
                        },
                        {
                              "ideology": 0,
                              "seniority": 3,
                              "opinion_type": "none",
                              "member": {
                                    "href": "https://api.oyez.org/people/samuel_chase",
                                    "ID": 15105,
                                    "last_name": "Chase",
                                    "thumbnail": {
                                          "size": 52231,
                                          "href": "https://api.oyez.org/sites/default/files/images/people/samuel_chase/samuel_chase.thumb.png",
                                          "id": 32759,
                                          "mime": "image/png"
                                    },
                                    "length_of_service": 5613,
                                    "view_count": 0,
                                    "identifier": "samuel_chase",
                                    "roles": [
                                          {
                                                "appointing_president": "George Washington",
                                                "href": "https://api.oyez.org/preson_role/scotus_justice/2749",
                                                "role_title": "Associate Justice of the Supreme Court of the United States",
                                                "type": "scotus_justice",
                                                "date_end": -5002970400,
                                                "id": 2749,
                                                "date_start": -5487933600,
                                                "institution_name": "Supreme Court of the United States"
                                          }
                                    ],
                                    "name": "Samuel Chase"
                              },
                              "href": "https://api.oyez.org/decision_vote/decision_vote/205611",
                              "vote": "none",
                              "joining": null
                        }
                  ],
                  "minority_vote": 0,
                  "winning_party": "Peck",
                  "decision_type": "majority opinion",
                  "majority_vote": 5,
                  "description": "Under the  Contracts Clause (Article 1, Section 10, Clause 1), states cannot rescind an agreement even if that agreement was reached illegally"
            }
      ],
      "href": "https://api.oyez.org/cases/1789-1850/10us87",
      "second_party": "John Peck",
      "first_party": "Robert Fletcher",
      "advocates": null,
      "description": "A case in which the Court held that a contract is still binding and enforceable, even if secured illegally.",
      "first_party_label": "Petitioner",
      "related_cases": null,
      "conclusion": "<p>In a unanimous opinion, the Court held that since the estate had been legally \"passed into the hands of a purchaser for a valuable consideration,\" the Georgia legislature could not take away the land or invalidate the contract. Noting that the Constitution did not permit bills of attainder or ex post facto laws, the Court held that laws annulling contracts or grants made by previous legislative acts were constitutionally impermissible.</p>\n",
      "facts_of_the_case": "<p>In 1795, the Georgia state legislature passed a land grant awarding territory to four companies. The following year, however, the legislature voided the law and declared all rights and claims under it to be invalid. In 1800, John Peck acquired land that was part of the original legislative grant. He then sold the land to Robert Fletcher three years later, claiming that past sales of the land had been legitimate. Fletcher argued that since the original sale of the land had been declared invalid, Peck had no legal right to sell the land and thus committed a breach of contract.</p>\n",
      "timeline": [
            {
                  "href": "https://api.oyez.org/case_timeline/case_timeline/52829",
                  "dates": [
                        -5045220000,
                        -5075546400,
                        -5075460000,
                        -5075373600,
                        -5075287200
                  ],
                  "event": "Argued"
            },
            {
                  "href": "https://api.oyez.org/case_timeline/case_timeline/52830",
                  "dates": [
                        -5042714400
                  ],
                  "event": "Decided"
            }
      ],
      "opinion_announcement": null,
      "second_party_label": "Respondent",
      "heard_by": [
            {
                  "href": "https://api.oyez.org/courts/marshall6",
                  "ID": 15247,
                  "members": [
                        {
                              "href": "https://api.oyez.org/people/john_marshall",
                              "ID": 15085,
                              "last_name": "Marshall",
                              "thumbnail": {
                                    "size": 53035,
                                    "href": "https://api.oyez.org/sites/default/files/images/people/john_marshall/john_marshall.thumb.png",
                                    "id": 32729,
                                    "mime": "image/png"
                              },
                              "length_of_service": 12570,
                              "view_count": 0,
                              "identifier": "john_marshall",
                              "roles": [
                                    {
                                          "appointing_president": "John Adams",
                                          "href": "https://api.oyez.org/preson_role/scotus_justice/2729",
                                          "role_title": "Chief Justice of the United States",
                                          "type": "scotus_justice",
                                          "date_end": -4244119200,
                                          "id": 2729,
                                          "date_start": -5330167200,
                                          "institution_name": "Supreme Court of the United States"
                                    }
                              ],
                              "name": "John Marshall"
                        },
                        {
                              "href": "https://api.oyez.org/people/william_cushing",
                              "ID": 15077,
                              "last_name": "Cushing",
                              "thumbnail": {
                                    "size": 52796,
                                    "href": "https://api.oyez.org/sites/default/files/images/people/william_cushing/william_cushing.thumb.png",
                                    "id": 32776,
                                    "mime": "image/png"
                              },
                              "length_of_service": 7527,
                              "view_count": 0,
                              "identifier": "william_cushing",
                              "roles": [
                                    {
                                          "appointing_president": "George Washington",
                                          "href": "https://api.oyez.org/preson_role/scotus_justice/2721",
                                          "role_title": "Associate Justice of the Supreme Court of the United States",
                                          "type": "scotus_justice",
                                          "date_end": -5027076000,
                                          "id": 2721,
                                          "date_start": -5677408800,
                                          "institution_name": "Supreme Court of the United States"
                                    }
                              ],
                              "name": "William Cushing"
                        },
                        {
                              "href": "https://api.oyez.org/people/samuel_chase",
                              "ID": 15105,
                              "last_name": "Chase",
                              "thumbnail": {
                                    "size": 52231,
                                    "href": "https://api.oyez.org/sites/default/files/images/people/samuel_chase/samuel_chase.thumb.png",
                                    "id": 32759,
                                    "mime": "image/png"
                              },
                              "length_of_service": 5613,
                              "view_count": 0,
                              "identifier": "samuel_chase",
                              "roles": [
                                    {
                                          "appointing_president": "George Washington",
                                          "href": "https://api.oyez.org/preson_role/scotus_justice/2749",
                                          "role_title": "Associate Justice of the Supreme Court of the United States",
                                          "type": "scotus_justice",
                                          "date_end": -5002970400,
                                          "id": 2749,
                                          "date_start": -5487933600,
                                          "institution_name": "Supreme Court of the United States"
                                    }
                              ],
                              "name": "Samuel Chase"
                        },
                        {
                              "href": "https://api.oyez.org/people/bushrod_washington",
                              "ID": 15093,
                              "last_name": "Washington",
                              "thumbnail": {
                                    "size": 42759,
                                    "href": "https://api.oyez.org/sites/default/files/images/people/bushrod_washington/bushrod_washington.thumb.png",
                                    "id": 32698,
                                    "mime": "image/png"
                              },
                              "length_of_service": 11339,
                              "view_count": 0,
                              "identifier": "bushrod_washington",
                              "roles": [
                                    {
                                          "appointing_president": "John Adams",
                                          "href": "https://api.oyez.org/preson_role/scotus_justice/2737",
                                          "role_title": "Associate Justice of the Supreme Court of the United States",
                                          "type": "scotus_justice",
                                          "date_end": -4421066400,
                                          "id": 2737,
                                          "date_start": -5400756000,
                                          "institution_name": "Supreme Court of the United States"
                                    }
                              ],
                              "name": "Bushrod Washington"
                        },
                        {
                              "href": "https://api.oyez.org/people/william_johnson",
                              "ID": 15059,
                              "last_name": "Johnson",
                              "thumbnail": {
                                    "size": 45940,
                                    "href": "https://api.oyez.org/sites/default/files/images/people/william_johnson/william_johnson.thumb.png",
                                    "id": 32779,
                                    "mime": "image/png"
                              },
                              "length_of_service": 11046,
                              "view_count": 0,
                              "identifier": "william_johnson",
                              "roles": [
                                    {
                                          "appointing_president": "Thomas Jefferson",
                                          "href": "https://api.oyez.org/preson_role/scotus_justice/2703",
                                          "role_title": "Associate Justice of the Supreme Court of the United States",
                                          "type": "scotus_justice",
                                          "date_end": -4273149600,
                                          "id": 2703,
                                          "date_start": -5227524000,
                                          "institution_name": "Supreme Court of the United States"
                                    }
                              ],
                              "name": "William Johnson"
                        },
                        {
                              "href": "https://api.oyez.org/people/brockholst_livingston",
                              "ID": 15111,
                              "last_name": "Livingston",
                              "thumbnail": {
                                    "size": 44786,
                                    "href": "https://api.oyez.org/sites/default/files/images/people/brockholst_livingston/brockholst_livingston.thumb.png",
                                    "id": 32714,
                                    "mime": "image/png"
                              },
                              "length_of_service": 5901,
                              "view_count": 0,
                              "identifier": "brockholst_livingston",
                              "roles": [
                                    {
                                          "appointing_president": "Thomas Jefferson",
                                          "href": "https://api.oyez.org/preson_role/scotus_justice/2755",
                                          "role_title": "Associate Justice of the Supreme Court of the United States",
                                          "type": "scotus_justice",
                                          "date_end": -4632314400,
                                          "id": 2755,
                                          "date_start": -5142160800,
                                          "institution_name": "Supreme Court of the United States"
                                    }
                              ],
                              "name": "Henry Brockholst Livingston"
                        },
                        {
                              "href": "https://api.oyez.org/people/thomas_todd",
                              "ID": 15039,
                              "last_name": "Todd",
                              "thumbnail": {
                                    "size": 41113,
                                    "href": "https://api.oyez.org/sites/default/files/images/people/thomas_todd/thomas_todd.thumb.png",
                                    "id": 32769,
                                    "mime": "image/png"
                              },
                              "length_of_service": 6854,
                              "view_count": 0,
                              "identifier": "thomas_todd",
                              "roles": [
                                    {
                                          "appointing_president": "Thomas Jefferson",
                                          "href": "https://api.oyez.org/preson_role/scotus_justice/2683",
                                          "role_title": "Associate Justice of the Supreme Court of the United States",
                                          "type": "scotus_justice",
                                          "date_end": -4540989600,
                                          "id": 2683,
                                          "date_start": -5133175200,
                                          "institution_name": "Supreme Court of the United States"
                                    }
                              ],
                              "name": "Thomas Todd"
                        }
                  ],
                  "court_start": -5133175200,
                  "view_count": 0,
                  "identifier": "marshall6",
                  "images": [
                        {
                              "size": 4355969,
                              "href": "https://api.oyez.org/sites/default/files/images/courts/marshall6.jpg",
                              "id": 78522,
                              "mime": "image/jpeg"
                        }
                  ],
                  "name": "Marshall Court (1807-1810)"
            }
      ],
      "manner_of_jurisdiction": "Writ of <i>certiorari</i>",
      "view_count": 1793,
      "lower_court": null,
      "justia_url": "https://supreme.justia.com/cases/federal/us/10/87/",
      "docket_number": "None",
      "ID": 62333,
      "written_opinion": [
            {
                  "author": null,
                  "judge_full_name": null,
                  "title": "Syllabus",
                  "id": 16171,
                  "href": "https://api.oyez.org/case_document/written_opinion/16171",
                  "justia_opinion_url": "https://supreme.justia.com/cases/federal/us/10/87/",
                  "judge_last_name": null,
                  "justia_opinion_id": 1907670,
                  "type": {
                        "value": "syllabus",
                        "label": "Syllabus"
                  }
            },
            {
                  "author": null,
                  "judge_full_name": null,
                  "title": "View Case",
                  "id": 16172,
                  "href": "https://api.oyez.org/case_document/written_opinion/16172",
                  "justia_opinion_url": "https://supreme.justia.com/cases/federal/us/10/87/case.html",
                  "judge_last_name": null,
                  "justia_opinion_id": 1907671,
                  "type": {
                        "value": "case",
                        "label": null
                  }
            }
      ],
      "question": "<p>Could the contract between Fletcher and Peck be invalidated by an act of the Georgia legislature?</p>\n",
      "citation": {
            "page": "87",
            "volume": "10",
            "year": "1810",
            "href": "https://api.oyez.org/case_citation/case_citation/27135"
      },
      "oral_argument_audio": null,
      "decided_by": {
            "href": "https://api.oyez.org/courts/marshall6",
            "ID": 15247,
            "members": [
                  {
                        "href": "https://api.oyez.org/people/john_marshall",
                        "ID": 15085,
                        "last_name": "Marshall",
                        "thumbnail": {
                              "size": 53035,
                              "href": "https://api.oyez.org/sites/default/files/images/people/john_marshall/john_marshall.thumb.png",
                              "id": 32729,
                              "mime": "image/png"
                        },
                        "length_of_service": 12570,
                        "view_count": 0,
                        "identifier": "john_marshall",
                        "roles": [
                              {
                                    "appointing_president": "John Adams",
                                    "href": "https://api.oyez.org/preson_role/scotus_justice/2729",
                                    "role_title": "Chief Justice of the United States",
                                    "type": "scotus_justice",
                                    "date_end": -4244119200,
                                    "id": 2729,
                                    "date_start": -5330167200,
                                    "institution_name": "Supreme Court of the United States"
                              }
                        ],
                        "name": "John Marshall"
                  },
                  {
                        "href": "https://api.oyez.org/people/william_cushing",
                        "ID": 15077,
                        "last_name": "Cushing",
                        "thumbnail": {
                              "size": 52796,
                              "href": "https://api.oyez.org/sites/default/files/images/people/william_cushing/william_cushing.thumb.png",
                              "id": 32776,
                              "mime": "image/png"
                        },
                        "length_of_service": 7527,
                        "view_count": 0,
                        "identifier": "william_cushing",
                        "roles": [
                              {
                                    "appointing_president": "George Washington",
                                    "href": "https://api.oyez.org/preson_role/scotus_justice/2721",
                                    "role_title": "Associate Justice of the Supreme Court of the United States",
                                    "type": "scotus_justice",
                                    "date_end": -5027076000,
                                    "id": 2721,
                                    "date_start": -5677408800,
                                    "institution_name": "Supreme Court of the United States"
                              }
                        ],
                        "name": "William Cushing"
                  },
                  {
                        "href": "https://api.oyez.org/people/samuel_chase",
                        "ID": 15105,
                        "last_name": "Chase",
                        "thumbnail": {
                              "size": 52231,
                              "href": "https://api.oyez.org/sites/default/files/images/people/samuel_chase/samuel_chase.thumb.png",
                              "id": 32759,
                              "mime": "image/png"
                        },
                        "length_of_service": 5613,
                        "view_count": 0,
                        "identifier": "samuel_chase",
                        "roles": [
                              {
                                    "appointing_president": "George Washington",
                                    "href": "https://api.oyez.org/preson_role/scotus_justice/2749",
                                    "role_title": "Associate Justice of the Supreme Court of the United States",
                                    "type": "scotus_justice",
                                    "date_end": -5002970400,
                                    "id": 2749,
                                    "date_start": -5487933600,
                                    "institution_name": "Supreme Court of the United States"
                              }
                        ],
                        "name": "Samuel Chase"
                  },
                  {
                        "href": "https://api.oyez.org/people/bushrod_washington",
                        "ID": 15093,
                        "last_name": "Washington",
                        "thumbnail": {
                              "size": 42759,
                              "href": "https://api.oyez.org/sites/default/files/images/people/bushrod_washington/bushrod_washington.thumb.png",
                              "id": 32698,
                              "mime": "image/png"
                        },
                        "length_of_service": 11339,
                        "view_count": 0,
                        "identifier": "bushrod_washington",
                        "roles": [
                              {
                                    "appointing_president": "John Adams",
                                    "href": "https://api.oyez.org/preson_role/scotus_justice/2737",
                                    "role_title": "Associate Justice of the Supreme Court of the United States",
                                    "type": "scotus_justice",
                                    "date_end": -4421066400,
                                    "id": 2737,
                                    "date_start": -5400756000,
                                    "institution_name": "Supreme Court of the United States"
                              }
                        ],
                        "name": "Bushrod Washington"
                  },
                  {
                        "href": "https://api.oyez.org/people/william_johnson",
                        "ID": 15059,
                        "last_name": "Johnson",
                        "thumbnail": {
                              "size": 45940,
                              "href": "https://api.oyez.org/sites/default/files/images/people/william_johnson/william_johnson.thumb.png",
                              "id": 32779,
                              "mime": "image/png"
                        },
                        "length_of_service": 11046,
                        "view_count": 0,
                        "identifier": "william_johnson",
                        "roles": [
                              {
                                    "appointing_president": "Thomas Jefferson",
                                    "href": "https://api.oyez.org/preson_role/scotus_justice/2703",
                                    "role_title": "Associate Justice of the Supreme Court of the United States",
                                    "type": "scotus_justice",
                                    "date_end": -4273149600,
                                    "id": 2703,
                                    "date_start": -5227524000,
                                    "institution_name": "Supreme Court of the United States"
                              }
                        ],
                        "name": "William Johnson"
                  },
                  {
                        "href": "https://api.oyez.org/people/brockholst_livingston",
                        "ID": 15111,
                        "last_name": "Livingston",
                        "thumbnail": {
                              "size": 44786,
                              "href": "https://api.oyez.org/sites/default/files/images/people/brockholst_livingston/brockholst_livingston.thumb.png",
                              "id": 32714,
                              "mime": "image/png"
                        },
                        "length_of_service": 5901,
                        "view_count": 0,
                        "identifier": "brockholst_livingston",
                        "roles": [
                              {
                                    "appointing_president": "Thomas Jefferson",
                                    "href": "https://api.oyez.org/preson_role/scotus_justice/2755",
                                    "role_title": "Associate Justice of the Supreme Court of the United States",
                                    "type": "scotus_justice",
                                    "date_end": -4632314400,
                                    "id": 2755,
                                    "date_start": -5142160800,
                                    "institution_name": "Supreme Court of the United States"
                              }
                        ],
                        "name": "Henry Brockholst Livingston"
                  },
                  {
                        "href": "https://api.oyez.org/people/thomas_todd",
                        "ID": 15039,
                        "last_name": "Todd",
                        "thumbnail": {
                              "size": 41113,
                              "href": "https://api.oyez.org/sites/default/files/images/people/thomas_todd/thomas_todd.thumb.png",
                              "id": 32769,
                              "mime": "image/png"
                        },
                        "length_of_service": 6854,
                        "view_count": 0,
                        "identifier": "thomas_todd",
                        "roles": [
                              {
                                    "appointing_president": "Thomas Jefferson",
                                    "href": "https://api.oyez.org/preson_role/scotus_justice/2683",
                                    "role_title": "Associate Justice of the Supreme Court of the United States",
                                    "type": "scotus_justice",
                                    "date_end": -4540989600,
                                    "id": 2683,
                                    "date_start": -5133175200,
                                    "institution_name": "Supreme Court of the United States"
                              }
                        ],
                        "name": "Thomas Todd"
                  }
            ],
            "court_start": -5133175200,
            "view_count": 0,
            "identifier": "marshall6",
            "images": [
                  {
                        "size": 4355969,
                        "href": "https://api.oyez.org/sites/default/files/images/courts/marshall6.jpg",
                        "id": 78522,
                        "mime": "image/jpeg"
                  }
            ],
            "name": "Marshall Court (1807-1810)"
      },
      "location": null,
      "name": "Fletcher v. Peck",
      "term": "1789-1850",
      "additional_docket_numbers": null,
      "loc_id": "http://www.loc.gov/item/usrep010087/",
      "loc_url": "http://www.loc.gov/item/usrep010087/",
      "simple_citation": "usrep010087",
      "shelf_id": "series: Volume 10 Call Number: KF101 Series: Contracts Law",
      "title": "U.S. Reports: Fletcher v. Peck, 10 U.S. (6 Cranch) 87 (1810).",
      "issues": [
            {
                  "issue": "supreme court"
            },
            {
                  "issue": "united states"
            },
            {
                  "issue": "court opinions"
            },
            {
                  "issue": "periodical"
            },
            {
                  "issue": "land titles"
            },
            {
                  "issue": "contracts law"
            },
            {
                  "issue": "court cases"
            },
            {
                  "issue": "judicial decisions"
            },
            {
                  "issue": "equity"
            },
            {
                  "issue": "law library"
            },
            {
                  "issue": "public lands"
            },
            {
                  "issue": "judicial review and appeals"
            },
            {
                  "issue": "contracts"
            },
            {
                  "issue": "government documents"
            },
            {
                  "issue": "bills and resolutions"
            },
            {
                  "issue": "law"
            },
            {
                  "issue": "common law"
            },
            {
                  "issue": "property rights"
            },
            {
                  "issue": "court decisions"
            },
            {
                  "issue": "u.s. reports"
            },
            {
                  "issue": "legislative powers"
            },
            {
                  "issue": "real estate"
            },
            {
                  "issue": "property"
            }
      ],
      "major_topics": [
            {
                  "major_topic": "contracts law"
            }
      ],
      "loc_pdf": "https://tile.loc.gov/storage-services/service/ll/usrep/usrep010/usrep010087/usrep010087.pdf"
}
```