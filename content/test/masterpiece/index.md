+++
title =  "Legal Research with AI: Part 6"
date = "2022-05-21T19:40:32.169Z"
description = "Control Model: A traditional statistical analysis of voting behavior in SPSS."
author = "Justin Napolitano"
image = "post-image.jpeg"
featuredimage = "post-image.jpeg"
categories = ['Legal Research', 'Research', 'SCOTUS', 'SPSS', 'Behavioral Modeling', 'Naive Bayesian', 'Statistical Analysis']
tags = ['python','legal', 'spss', 'scotus', 'statistics']
series = ['Legal Research with AI']
+++


## Introduction

Currently, my server is mining data from the neo4j graph database.

This post contains a control model completed in SPSS that will serve as the base line for comparison to Ml models.  It includes a short literature review of the theoritical foundation of the Attitudinal Model of Judicial Behavior.

   
## Hypothesis
When considering the individual Supreme Court Justices, their voting behavior may be best described by the interaction between their ideological precepts and the facts of the case.  Their vote will not be dictated entirely by the constraint of precedent. 

## Experimental Design
 In this paper, the legal model is tested against the attitudinal model.   The intent is to best describe the process of Supreme Court decision making in relationship to Masterpiece Cakeshop, Ltd. v. Colorado Civil Rights Commission {cite}`masterpiececake`.  

### The Legal Model

The Legal Model consists of three major components: 

1. precedent [^need]
2. text (constitutional and statutory provisions) [^need] 
3. legislative intent. [^need]  

The initial analysis of Masterpiece Cakeshop Ltd. v. Colorado Civil Rights Commission {cite}`masterpiececake` will consist of an argument dependent on all three. 


### The Attitudinal Model

The proposed attitudinal model will derive ideological values for the individual justices according to subject area [^reference].  This is accomplished by cross-referencing the current Supreme Court justices’ votes on the merits across time [^reference].  The first set of scores describe general voting behavior.  The next by first amendment cases.  Finally, by first amendment cases controlling for establishment [^const] and free exercise [^const] clause. and external situations [^reference].  When applying these to the facts of the case in Masterpiece Cakeshop Ltd. vs. Colorado Civil Rights Board (2018) it is expected that ideological scores will predict the outcome.  


## Legal Model Case Study
Write an intro.  Facts, text, 

### The Facts of the Case


The facts of the case in this instance are pulled directly from the syllabus of the Supreme Court Opinion {cite}`masterpiececake`: 

> Masterpiece Cakeshop, Ltd., is a Colorado bakery owned and operated by Jack Phillips, an expert baker and devout Christian. In 2012, he told a same-sex couple that he would not create a cake for their wedding celebration because of his religious opposition to same-sex marriages—marriages that Colorado did not then recognize—but that he would sell them other baked goods, e.g., birthday cakes. The couple filed a charge with the Colorado Civil Rights Commission (Commission) pursuant to the Colorado Anti-Discrimination Act (CADA), which prohibits, as relevant here, discrimination based on sexual orientation in a “place of business engaged in any sales to the public and any place offering services . . . to the public." Under CADA’s administrative review system, the Colorado Civil Rights Division first found probable cause for a violation and referred the case to the Commission. The Commission then referred the case for a formal hearing before a state Administrative Law Judge (ALJ), who ruled in the couple’s favor. In so doing, the ALJ rejected Phillips’ First Amendment claims: that requiring him to create a cake for a same-sex wedding would violate his right to free speech by compelling him to exercise his artistic talents to express a message with which he disagreed and would violate his right to the free exercise of religion.


### The Pertinent Text


The first step of the test is to test Mr. Phillips claims against pertinent text of the controlling statutory and constitutional provisions.  Therefore, the relevant texts relating to the free speech claims are:  
1. The First Amendment of the Constitution [^const] 
2. The Colorado Public Accommodation law {cite}:`crs-title24-art-34-part-6-section 601-604-2016`.  

These will be tested against the claim that the Colorado Law unduly burdens Mr. Phillips by abridging his free exercise of religion, as well as his freedom of speech.  [^expand]

#### The First Ammendment Text

I begin with the First Amendment [^const].  Due to its brevity, I include the entire text: 

 > Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise thereof; or abridging the freedom of speech, or of the press; or the right of the people peaceably to assemble, and to petition the Government for a redress of grievances. (U.S. Const. amend I)

#### Colorado State Law Title 24, Article 34, Part 6, Section 601-604 2016

The pertinent clause of the Colorado State Law in question reads:

> It is a discriminatory practice and unlawful for a person, directly or indirectly, to refuse, withhold from, or deny to an individual or a group, because of disability, race, creed, color, sex, sexual orientation, marital status, national origin, or ancestry, the full and equal enjoyment of the goods, services, facilities, privileges, advantages, or accommodations of a place of public accommodation (Colorado Revised Statute, Title 24, Article 34, Part 6, Section 601-604 2016).


### Standing  

Based simply on textual grounds, Mr. Phillips’ free exercise, and freedom of speech claims are completely unfounded.  The first amendment as written does not protect the individual resident of an individual state from undue abridgements of personal religious and speech freedoms.  If we adopt the standard of incorporation as written into the precedent the first amendment still does not seem to support the claims.1  Speech, if understood according to Webster, is “communication or expression of thoughts in spoken words (Webster's New World 2016).” The action of making a cake, cannot be in any way considered speech by this definition. speech.  Symbolic speech, whatever that means, is not written into the Constitution.  


#### The First Ammendment Standing
At first reading, Mr. Phillips claim [^claim] does not seem to be legitimate.  If in fact the Colorado Law abridges religious freedoms, or individual speech in any way the amendment reads that “Congress shall make no law”.  At least when reading the text of the First Amendment as plainly as possible it does not apply directly to the case at hand. As a matter of fact, it does not apply to state in any capacity. The difficulty however, is that the Court has incorporated into the common law this amendment.  Therefore, it considered applicable to the states, and thus operable upon the residents of the individual states.  Forgoing this truth, we also run into a few textual problems.  For instance, how is it that speech is defined? Or exactly what constitutes a prohibition of the free exercise of religion?  These questions may only be answer by consulting precedent.  

#### Colorado State Law Standing

Contrary to Mr. Phillips’ claim the law does not seem to unduly burden any religious freedoms, nor speech in general.  Rather, it is a generally applicable law, that extends protections in places of public accommodation to people according to sexual-orientation.  Reading this in contrast to the First Amendment, there are no direct violations.

### Legislative Intent

If the Court relied entirely on the textual evidence to judge, it is apparent that the case would not have been heard by the bench. However, this is obviously not the case.  As such, Legislative Intent must also be considered in this analysis.  This section will attempt to discover the intent behind the First Amendment in order to judge Mr. Philips’ claims against original intent.  


#### The First Ammendment Intent

The First Amendment along with the remaining nine were first introduced to the floor of Congress in 1789 to address the concern that specific individual liberties could be eroded by the powers of the national congress. According to James Madison, in order to limit the power of the legislature.  The case being that it is the most powerful branch, and therefore most likely to be abused (Lloyd 1789).  At the behest of the representatives of the individual states, as well as their ratification committees, the National Congress in order to ratify the Constitution agreed to ratify a Bill of Rights. 

Each individual clause of the amendment is important to the discussion.  For the purpose of this paper, I will discuss the legislative history of the Establishment and Free Exercise Clauses, as well as the Freedom of Speech Clauses.  Then a short discussion on the drafting process of the entire amendment will be had.  

#### Freedom of Speech

The ideological and textual foundations for the free speech clauses come from English heritage.  For instance, the English Bill of Rights, drafted in 1689, states “that the freedome of speech and debates or proceedings in Parlyament ought not to be impeached or questioned in any court or place out of Parlyament (1 Will. And Mar. Sess. 2, c. 2.)”

The individual states in their constitutions drafted protection for at least the “freedom of the press.” [^laws]  The state of Pennsylvania in their 1790 Constitution states that:

> The printing presses shall be free to every person who undertakes to examine the proceedings of the legislature, or any branch of government: And no law shall ever be made to restrain the right thereof.  The Free communication of the thoughts and opinions is one of the invaluable rights of man; and every citizen may freely speak, write and print on any subject, being responsible for the abuse of that liberty.  (Dallas 1791, xxxiv)


Evident here is the strong common law and statutory practice of protection of the rights of the individual to publish material no matter the content, however, there does not seem to be a protection for symbolic expressions of speech such as the production of a cake.  

The state ratification committees offer the best insight into the matter of free speech, as it meant to those most concerned with protecting that right.  The Honorable James Lincoln, of South Carolina puts the point most succinctly:


> Why in this Constitution, is a total silence with regard to the liberty of the press?  Was it forgotten? Impossible!  Then it must have been purposely omitted…. The Liberty of the press was the tyrants scourge — it was the true friend and firmest supporter of civil liberty; therefore, why pass it by in silence?... Pray, sir, what security have we for a republican form of government, when it depends on the mere will and pleasure of a few men, who, with an army, navy, and rich treasury at their back, may change and alter it as they please?  It may be said they will be sworn.  Sir, the king of Great Britain, at his coronation, swore to govern his subjects with justice and mercy.  We were then his subjects, and continued so for a long time after.  He would be glad to know how he observed his oath.  If, then, the king of Great Britain forswore himself, what security have we that a future President and four or five senators — like himself — will think more solemnly of so sacred an obligation than he did?   (Elliot 1888, 314-316)


The most obvious concern is the failure of the Constitution to draft specific protections to secure the individual states from the type of tyranny experienced under the English Crown.  So too is a bit of realism present.  How is it that men, men of high rank, can be expected to uphold their oaths to govern with regard to the people?  When it is likely that men that acquire power will in many cases do the utmost to retain that power.  It is difficult to make the argument that these men had much of a consideration for individual speech, or any form of symbolic speech [^symbolic-speech]

The Congressional accounts support the same basic idea.  James Madison proposed to the House, that the “people shall not be deprived or abridged of their right to speak, to write, or to publish their sentiments; and the freedom of the press, as one of the great bulwarks of liberty, shall be inviolable (Lloyd 1789).  Roger Sherman, also put to the floor, that “people have certain natural rights which are retained by them when they enter into society. Such are the rights… of Speaking, writing and publishing their Sentiments with decency and freedom (Lloyd 1789).”   There is no apparent concern for symbolic forms of speech.  Rather, the idea is that someone may privately write and say what he so wishes, and publish that material if one so chooses.  
	
The overarching intent of the Free Speech clause, appears to be an intent to forbid the federal government from restricting access to free presses.  The concern is almost exclusively focused on published material, and the fact that a free press enables the people of a nation to challenge the acts of government.  To restrict this right, in the eyes of some members of the congress, and the state ratification committees, was to in effect establish a tyrannical government.  The English Bill of Rights, State Constitutions, and the accounts of the State Ratification Committees all support this.  

The conditional clauses within the state constitutions also point to the fact, that speech was not to be construed to enable a person to act in a way that is harmful to the public welfare.  State laws passed in order to improve the well being of the general public could not be abrogated by individuals claiming a free speech exemption.  In reference to Mr. Phillips’ claims an original intent lens, at best guess [^impossible], would not support an individual protection from state public accommodation laws on free speech grounds.  

#### Establishment and Free Exercise Clauses

Again, the English heritage of founders of the United States is relevant to the discussion.  The English Bill of Rights reads, “that the commission for erecting the late courts of commissioners of ecclesiastical causes and all other commissions and courts of like nature are illegal and pernicious (1 Will. and Mary. Sess. 2, c. 2).” [^william-and-mary]

Also, certain State constitutions prohibit religious tests necessary to hold office, as well as the imposition of any religious belief upon inhabitants.  Georgia’s in particular, “All persons whatever shall have the free exercise of their religion; provided it be not repugnant to the peace and safety of the State; and shall not, unless by consent, support any teacher, or teachers, except those of their own profession…. No clergyman, of any denomination, shall be allowed a seat in the legislature (Watkins and Watkins 1800, 15-16).” Also, important is the state of New York’s 1777 constitution which states, “that the free Exercise and Enjoyment of religious Profession and Worship, without Discrimination or Preference, shall forever hereafter be allowed within this state to all Mankind.” Noticeable is the conditional clause, citing: Provided, that the Liberty and Conscience hereby granted, shall not be so construed, as to excuse Acts of Licentiousness, or justify Practices inconsistent with the Peace or Safety of this State (The State of New York 1789, 13).” A number of other states follow in like fashion. [^laws2]

An intent to separate civil and political life is also apparent at the first congress.  For instance, at first drafting what became the establishment clause read, “The civil rights of none shall be abridged on account of religious belief or worship, nor shall any national religion be established, nor shall the full and equal rights of conscience be in any manner, or any pretext infringed (Lloyd 1789).”  A later draft also read, “Congress shall make no law establishing articles of faith or a mode of worship, or prohibiting the free exercise of religion, or abridging the freedom of speech, or the press, or the right of the people peaceable to assemble, and petition to the Government for the redress of grievances (Lloyd 1789).”

Together, these provide little evidence into the intention of the legislators present at the first congress.  The first draft, quite different from the final, implies a respect for both the free exercise of religion, and for free exercise of action according to the dictate of conscience.  As a summary of Mr. Samuel Huntington’s concern reads, “he hoped therefore the amendment would be made in such a way as to secure the rights of conscience, and a free exercise of the rights of religion, but not to patronize those who profess no religion at all (Lloyd 1789).” Thus, concern for both religious exercise, as well as non-religious seems to be equally supported by at least Mr. Huntington.  Governor Randolph of Virginia puts this same convention more forwardly in stating that, “a mutual toleration, and a persuasion that no man has the right to impose his opinion on other” is his intent behind the ratification of what became the first amendment (Elliot 1888).

However, the next draft removes this consideration, and limits the wording to include only protections for the free-exercise of religion.  Freedom of consciousness, whatever that they may mean is dropped.  A series of other drafts may be considered, as may conflicting pamphlets but the pressing reality is that the members of the first congress, as well as the state ratification committees, and the general public at large, all had different concerns.  Who is considered to be authoritative on this matter is dependent upon the values of the individual reader.  Therefore, there cannot be one legislative intent, but instead a diversity of intents that converged about a single piece of legislation.  

If one were to guess, which is the best that can be done on the matter, the intent behind the establishment clause was to protect the individual states from usurpation of powers by the federal government of powers historically held by the states.  The protections for religion, speech, assembly, and redress, grant to the states special protections in order to further weaken the federal government.  There is not a unanimous application of these rights to all individual inhabitants within the United States.    No, instead, a blanket restriction was imposed upon the federal government, in order to allow the states to manage these affairs as they saw fit.  If a justice were to consult this original intention, Mr. Philips’ claims would be superfluous, as the amendment would not be binding on the state of Colorado.  

### Precedent

#### Analysis of Case Law

To test Mr. Phillips’ claim to a freedom of speech, and a free exercise exemption, this section of the paper will analyze the doctrines created by the Supreme Court in regard to Privacy, Establishment, Free Exercise, and the Freedom of Contract.

#### Establishment of Clause

Lemon v. Kurtzman is the authority which the court recognizes as the standard by which to test laws for Establishment Clause violations.  The “Lemon Test” states three rules.  “First, the statute must have a secular legislative purpose; second, its principal or primary effect must be one that neither advances nor inhibits religion; Finally, the statute must not foster an excessive government entanglement with religion (Lemon v. Kurtzman, 1971) “In order to determine whether the government entanglement with religious is excessive, we must examine the character and purpose of the institutions that benefitted, the nature of the aid the state provides, and the resulting relationship between the government and the religious authority (Lemon v. Kurtzman, 1971).”  The Colorado state law in question, does not in any way violate these provisions.  


For example, it may not be construed to have any other purpose than a secular one.  Secondly, the primary effect does not inhibit nor advance religion.  The primary purpose only protects individuals from discrimination in place of public accommodation.  Third, the law does not entangle the government, federal or state, with religion.  In effect, the government, no matter the degree of separation, is not entangled with any church, mosque, or any other form of religion.

#### Free Exercise

The Free Exercise claim is not as easily defeated.  A number of cases must be reviewed in order to conclude whether the Colorado law is in violation of this clause (U.S. Const. amend. I cl.1)


##### Reynolds v. United States 1879

The first case under consideration is Reynolds v. United States (1879), in which laws prohibiting bigamy were brought under scrutiny when challenged by members of the Church of Latter Day Saints.  To challenge the conviction, which was considered, as it is at present antithetical to publically accepted morality the Court argued that “laws are made for the government of actions, and while they cannot interfere with mere religious belief and opinions, they may with practices (Reynolds v. United States, 1879)” in order to promote the general welfare of the people.  To permit otherwise “would be to make the professed doctrines of religious belief superior to the law of the land, and in effect to permit every citizen to become a law unto himself (Reynolds v. United States, 1879).”  

##### Employment Division v. Smith 1990

This position is reiterated in Employment Div. v. Smith (1990) in which the court deliberated on the validity of a Seattle State law’s prohibition on providing unemployment benefits to individuals found to have used schedule I substance despite a claim to a religious exemption.  The appellant sought to reverse the verdict of Reynolds.  The Court did not budge.  To force the state to violate its own laws at the behest of an individual claiming religious exemptions for specific practices in effect does put the government behind the promotion of the claimant’s religious beliefs.  In fact, “it is a permissible reading of U.S Const. Amend. I to say that if prohibiting the exercise or religion is not the object of a law, but merely the incidental effect of a generally applicable and otherwise valid provision, the First Amendment has not been offended (Employment Div. v. Smith, 1990).”

##### Hobby Lobby, Inc v. Burwell 2014

The court shifted however in Hobby Lobby, Inc v. Burwell which the Supreme Court violated the spirit of previous decisions in response to Congress’ passage of the Religious Land Use and Institutionalized Persons Act, the RLUIPA. Which is “in an obvious effort to effect a complete separation from First Amendment case law (Hobby Lobby, Inc v. Burwell, 2014).” The Court did not strike the law as they had done City of Boerne v. Flores (1997).  Instead they validated it despite the fact “the powers of the legislature are defined and limited; and that those limits may not be mistaken (City of Boerne v. Flores, 1997).”  Unlike the consensus in Employment Div. v. Smith (1990), that a rule of general applicability may supersede one’s free exercise rights, the court found in favor of the corporate entity Hobby Lobby’s stance that the imposition of fines as punishment for not providing contraceptive coverage to female employees is not the “least restrictive means of furthering” a government interest.  

##### Free Exercise Mr. So and So's Claim

Considering the current claim, is it that the Colorado Law unduly inhibits the free exercise of religious belief?  No, it does not in any way.  By way of Lemon v. Kurtzman (1971), Reynolds v. United States (1879), and Employment Div. v. Smith (1990), the Colorado Public Accommodation law passes the test of general applicability.  However, the only precedent which may challenge its constitutionality is Hobby Lobby, Inc v. Burwell (2014).  Nonetheless, the Colorado Law may be considered the least restrictive means to further the public accommodation protections according to sexual-orientation.  To accomplish the same ends in any way less restrictive would require the law to be struck from the books.  

#### Privacy 

The right to marriage, well the right for same-sex couples to marry is a right founded in the doctrine of privacy and supported by the Fourteenth Amendment.  Obergefell v. Hodges (2015) the ruling which enabled same-sex couples to marry is the culmination of a development of a doctrine which proposes that institutions understood to be fundamental to ordered liberty ought not to be excessively regulated by the Congress (Palko v. Connecticut, 1937).   A string of cases in which the Court came to adopt the position that consenting adults of nontraditional relationships ought to receive the same protections under the law as those of traditional relationships rationalize the ruling. [^tradition]  

##### Griswold v. Connecticut 1965

In Griswold v. Connecticut (1965) it was found that a consenting couple may receive counseling from a planned parenthood representative with regard to birth control.  The right of that couple to act according to their discretion is fundamental to the institution of marriage.  The court could not find a rational government interest to infringe upon that sacred barrier. 

##### Loving v. Virginia 1967

Accordingly, the Court ruled in Loving v. Virginia (1967) that the rights afforded to white couples and black couples, could not be excluded from couples of mixed races.  Marriage is a fundamental right.  Therefore, it cannot be awarded only to select classes. Rather it is a right afforded to each individual of the United States.  The Fourteenth Amendment ensures that all people are afforded equal protection under the law.  To violate this principle is to violate the constitution. 

##### Lawrence v. Texas 2003

Lawrence v. Texas (2003) applied this principle to same sex couples.  It was found that sodomy laws in general restrict the ability for male same-sex couples to fully realize intimacy.  The laws unduly affected a single class of individuals without reason except to eliminate a socially unaccepted behavior from the private lives of two consenting adults.  The court could find no basis for the ban apart from undue bias directed at same-sex couples.  

##### Obergefell v. Hodges 2015 

The ultimate realization of the privacy protections and Fourteenth Amendment jurisprudence is found in Obergefell v. Hodges (2015) The court here found that “the right to marry is a fundamental right inherent in the liberty of the person (Obergefell v. Hodges, 2015).”  To disallow a same sex couples the right to marriage “denies individual dignity and autonomy (Obergefell v. Hodges, 2015).” to a subclass of citizens without rational basis.  In Obergefell v. Hodges (2015) “under the Due Process and Equal Protections Clauses of the Fourteenth Amendment couples of the same-sex may not be deprived” of their right to marry and to share the same privileges of same-sex couples.

##### Privacy and Mr. So and So's Claim

According then to the Privacy doctrine, and namely Obergefell v. Hodges the right for gay couples to marry is fundamental.  They must then receive the same privileges and protections of all other married couples.  Without even the Colorado Law in place, I would argue that the Privacy Doctrine in of itself protects gay couples from the type of discrimination experienced by Mr. Charlie Craig and Mr. Dave Mullins.  The sanctity of the institution of marriage no matter those whom enter into it is fundamental to the idea of liberty in this country. To violate that sanctity when two gay men marry is to violate the holding of Obergefell and more heinously the dignity of two individuals. 

#### Freedom to Contract

There may be a case for the individual right to bargain for the terms of one’s contracts free from the regulation of the government, but the court has already spoken on this matter.  “The power… to restrict freedom of contract may be exercised in the public interest (West Coast Hotel Co. v. Parrish, 1937) Also, the authority of the government to regulate products that affect interstate commerce has been affirmed in United States v. Darby (1941). The real question here is whether a state government may regulate services in places of public accommodation? 

The answer is a resounding yes. The Federal government for instance may do so when commerce is affected.  The two most important cases for the purpose of this paper are Katzenbach v. McClung (1964) and Heart of Atlanta Motel, Inc. v. United States (379 U.S. 241, 1964). These cases both rest on the validity of Title II of the Civil Rights Act of 1964 which states “all Persons shall be entitled to the full and equal enjoyment of the goods, services, facilities, privileges, advantages, and accommodations of any place of public accommodation.”  Public accommodation is defined as “any inn, hotel, motel, or other establishment which provides lodging to transient guests.  Any Restaurant, cafeteria, lunchroom, lunch counter, soda fountain, or other facility principally engaged in selling food for consumption on the premises. (42 U.S.C. S 2000a(a), 42 U.S.C. S 2000a(b)).  


##### Katzenbach v. McClung 1964 

In Katzenbach v. McClung (1964) the Court recognized “that discrimination in restaurants has a direct and highly restrictive effect upon interstate travel… This results because discriminatory practices prevent Negroes from buying prepared food… except in isolated and unkempt restaurants and under unsatisfactory and often unpleasant conditions (Katzenbach v. McClung, 1964).”  The outcome of which is the treatment of Blacks as second-class citizens not deserving the standards of decency enjoyed by their White peers. As the Congress enjoys “the power to make all laws which shall be necessary and proper for carrying into execution” it’s Commercial and Spending powers, Congress may regulate “those activities intrastate which so affect interstate commerce… to the attainment of a legitimate end (Katzenbach v. McClung, 1964).” 

##### Heart of Atlanta Motel, Inc, v. United States 1964 

Heart of Atlanta Motel, Inc. v. United States (1964) reiterates the opinion of Katzenbach v. McClung (1964), but further specifies when the Congress may in fact regulate commercial services.  “The only questions are (1) whether Congress had a rational basis for finding that racial discrimination... affected commerce, and (2) if it had such a basis, whether the means it selected to eliminate that evil reasonable and appropriate (Heart of Atlanta Motel, Inc. v. United States, 1964).”  In the case of the segregation of hotels the Congress is well within its bounds to manage the way in which proprietors treat their customers, in order to avoid the evil of segregation.  It is not a stretch to apply the same principles to support the right of a state’s legislature to ensure that no discrimination occurs on the basis of sexual-orientation. 

##### Freedom to Contract and Mr. So and So's claim

In the case of the individual states, their police powers alone allow them to enforce public accommodation laws by way of the 10th amendment.  The barometer in the case of Masterpiece Cake (2018)  is whether the Colorado law protects the welfare, safety, and health of the public at large.  Obviously, a state law which purports to protect the general welfare, and safety of all people can be said to meet this standard.  


(attitudinal-case-study)=
## Attitudinal Model Case Study
Write an intro.  Facts, text, 

### Methodology

To build a model that takes into account the subjective attitudes of the Supreme Court Justices. I use the Washington University Law Database (Spaeth, Epstein, et al. 2017) that takes into account the individual decisions of each justice in order to determine their ideological value across time.   I then test these values against the facts, including attitudinal objects, and attitudinal situations, of Masterpiece Cake LTD. v. Colorado Civil Rights Commission (2018)

#### Ideological Score by Justice 
To determine a justice’s ideological score I test their votes across time to determine whether they vote conservatively or liberally.  A simple mean value between one and two is then generated.  The closer to one a justice votes the more conservative.  Alternatively, the closer to two the value, the more liberal.  The results for the individual justices are included in 
the chart below.  

###### Table
 
 Justice | Mean | N | Std. Deviation | Variance
 ---|---|---|---|---
 AMKennedy | 1.42 | 2668 | 0.493 | 0.243
 CThomas | 1.32 | 2179 | 0.468 | 0.219
 RBGinsburg | 1.6 | 1964 | 0.491 | 0.241
 SGBreyer | 1.56 | 1848 | 0.496 | 0.246
 JGRoberts | 1.42 | 913 | 0.493 | 0.243
 SAAlito | 1.36 | 874 | 0.481 | 0.232
 SSotomayor | 1.62 | 600 | 0.487 | 0.237
 EKagan | 1.59 | 486 | 0.492 | 0.242
 NMGorsuch | 1.18 | 17 | 0.393 | 0.154
 Total | 1.47 | 11549 | 0.499 | 0.249



#### Ideological Score by Justice First Ammendment 
Similarly, I derive ideological values according to voting patterns relating to first amendment cases.  The results are printed in the following chart.  

##### Table

 Justice | issue area of case (coarse) | Mean | N | Std. Deviation | Variance
 ---|---|---|---|---|---
 AMKennedy | First Amendment | 1.47 | 167 | 0.5 | 0.25
 CThomas | First Amendment | 1.33 | 127 | 0.472 | 0.223
 RBGinsburg | First Amendment | 1.68 | 112 | 0.469 | 0.22
 SGBreyer | First Amendment | 1.55 | 108 | 0.5 | 0.25
 JGRoberts | First Amendment | 1.51 | 47 | 0.505 | 0.255
 SAAlito | First Amendment | 1.42 | 43 | 0.499 | 0.249
 SSotomayor | First Amendment | 1.67 | 33 | 0.479 | 0.229
 EKagan | First Amendment | 1.67 | 27 | 0.48 | 0.231
 NMGorsuch | First Amendment | 2 | 1 | . | .
 Total | First Amendment | 1.51 | 665 | 0.5 | 0.25


#### Ideological Score by Justice by Individual Issue Area
Finally, ideological scores are derived by issue area.  For the purpose of this discussion this is equivalent to an evaluation of the individual attitude-situations as they relate to the facts of the case.  The results are below:


##### Table

Justice | issue area of case (coarse) | Issue Area Of Case (Fine) | Mean | N | Std. Deviation | Variance
---|---|---|---|---|---|---
AMKennedy | First Amendment | Free Exercise Of Religion | 1.71 | 14 | 0.469 | 0.22
 |  | Establishment Of Religion | 1.23 | 13 | 0.439 | 0.192
 |  | Total | 1.48 | 27 | 0.509 | 0.259
 | Total | Free Exercise Of Religion | 1.71 | 14 | 0.469 | 0.22
 |  | Establishment Of Religion | 1.23 | 13 | 0.439 | 0.192
 |  | Total | 1.48 | 27 | 0.509 | 0.259
CThomas | First Amendment | Free Exercise Of Religion | 1.91 | 11 | 0.302 | 0.091
 |  | Establishment Of Religion | 1.1 | 10 | 0.316 | 0.1
 |  | Total | 1.52 | 21 | 0.512 | 0.262
 | Total | Free Exercise Of Religion | 1.91 | 11 | 0.302 | 0.091
 |  | Establishment Of Religion | 1.1 | 10 | 0.316 | 0.1
 |  | Total | 1.52 | 21 | 0.512 | 0.262
RBGinsburg | First Amendment | Free Exercise Of Religion | 1.56 | 9 | 0.527 | 0.278
 |  | Establishment Of Religion | 2 | 9 | 0 | 0
 |  | Total | 1.78 | 18 | 0.428 | 0.183
 | Total | Free Exercise Of Religion | 1.56 | 9 | 0.527 | 0.278
 |  | Establishment Of Religion | 2 | 9 | 0 | 0
 |  | Total | 1.78 | 18 | 0.428 | 0.183
SGBreyer | First Amendment | Free Exercise Of Religion | 1.78 | 9 | 0.441 | 0.194
 |  | Establishment Of Religion | 1.67 | 9 | 0.5 | 0.25
 |  | Total | 1.72 | 18 | 0.461 | 0.212
 | Total | Free Exercise Of Religion | 1.78 | 9 | 0.441 | 0.194
 |  | Establishment Of Religion | 1.67 | 9 | 0.5 | 0.25
 |  | Total | 1.72 | 18 | 0.461 | 0.212
JGRoberts | First Amendment | Free Exercise Of Religion | 2 | 7 | 0 | 0
 |  | Establishment Of Religion | 1 | 2 | 0 | 0
 |  | Total | 1.78 | 9 | 0.441 | 0.194
 | Total | Free Exercise Of Religion | 2 | 7 | 0 | 0
 |  | Establishment Of Religion | 1 | 2 | 0 | 0
 |  | Total | 1.78 | 9 | 0.441 | 0.194
SAAlito | First Amendment | Free Exercise Of Religion | 2 | 6 | 0 | 0
 |  | Establishment Of Religion | 1 | 2 | 0 | 0
 |  | Total | 1.75 | 8 | 0.463 | 0.214
 | Total | Free Exercise Of Religion | 2 | 6 | 0 | 0
 |  | Establishment Of Religion | 1 | 2 | 0 | 0
 |  | Total | 1.75 | 8 | 0.463 | 0.214
SSotomayor | First Amendment | Free Exercise Of Religion | 1.5 | 6 | 0.548 | 0.3
 |  | Establishment Of Religion | 2 | 2 | 0 | 0
 |  | Total | 1.63 | 8 | 0.518 | 0.268
 | Total | Free Exercise Of Religion | 1.5 | 6 | 0.548 | 0.3
 |  | Establishment Of Religion | 2 | 2 | 0 | 0
 |  | Total | 1.63 | 8 | 0.518 | 0.268
EKagan | First Amendment | Free Exercise Of Religion | 1.8 | 5 | 0.447 | 0.2
 |  | Establishment Of Religion | 2 | 1 | . | .
 |  | Total | 1.83 | 6 | 0.408 | 0.167
NMGorsuch | First Amendment | Free Exercise Of Religion | 2 | 1 | . | .
 |  | Total | 2 | 1 | . | .
 | Total | Free Exercise Of Religion | 2 | 1 | . | .
 |  | Total | 2 | 1 | . | .
Total | First Amendment | Free Exercise Of Religion | 1.78 | 68 | 0.418 | 0.174
 |  | Establishment Of Religion | 1.46 | 48 | 0.504 | 0.254
 |  | Total | 1.65 | 116 | 0.48 | 0.231
 | Total | Free Exercise Of Religion | 1.78 | 68 | 0.418 | 0.174
 |  | Establishment Of Religion | 1.46 | 48 | 0.504 | 0.254
 |  | Total | 1.65 | 116 | 0.48 | 0.231




### Expected Results

In an attempt to replicate the results of Masterpiece Cakeshop Ltd. v. Chicago Civil Rights Commission (2018) I will simply consult the three ideological values above.  If a justice scores below a 1.5 in any area, then they will be expected to vote conservatively.  Conversely if a score above 1.5 is observed the justice is expected to vote liberally.  


In context, A liberal vote will found in favor of the Mr. Charlie Craig and his partner, Mr. Dave Mullins.  The following variables describe liberal voting preferences as they relate to the case.  Pro-civil liberties or civil rights, pro-neutrality in establishment clause cases, pro-underdog, anti-owner, anti-business, pro-government, pro-exercise of judicial action, and pro-judicial activism. A conservative vote is in favor of Mr. Philips, the Colorado baker. Conservatism in context is described as opposite the above liberal values.  


#### Justice Vote According to General Ideological Score


##### Table

Justice | Score | Vote
---|---|---
AMKennedy | 1.42 | Cons.
CThomas | 1.32 | Cons.
RBGinsburg | 1.6 | Lib.
SGBreyer | 1.56 | Lib.
JGRoberts | 1.42 | Cons.
SAAlito | 1.36 | Cons.
SSotomayor | 1.62 | Lib.
EKagan | 1.59 | Lib.
NMGorsuch | 1.18 | Cons.
Total | 1.47 | Cons.




#### Justice Votes by First Amendment 



##### Table 

Justice | issue area of case (coarse) | Score | Vote
---|---|---|---
AMKennedy | First Amendment | 1.47 | Cons.
CThomas | First Amendment | 1.33 | Cons.
RBGinsburg | First Amendment | 1.68 | Lib.
SGBreyer | First Amendment | 1.55 | Lib.
JGRoberts | First Amendment | 1.51 | Lib.
SAAlito | First Amendment | 1.42 | Cons.
SSotomayor | First Amendment | 1.67 | Lib.
EKagan | First Amendment | 1.67 | Lib.
NMGorsuch | First Amendment | 2 | Cons.
Total | First Amendment | 1.51 | Lib.
 | Total | 1.51 | Lib.



#### Justice Votes by Issue Area


##### Table 


Justice Identification Number | Issue Area Of Case (Coarse) | Issue Area Of Case (Fine) | Score | Vote
---|---|---|---|---
Amkennedy | First Amendment | Free Exercise Of Religion | 1.71 | Lib.
 |  | Establishment Of Religion | 1.23 | Cons.
 |  | Total | 1.48 | Cons.
Cthomas | First Amendment | Free Exercise Of Religion | 1.91 | Lib.
 |  | Establishment Of Religion | 1.1 | Cons.
 |  | Total | 1.52 | Lib
Rbginsburg | First Amendment | Free Exercise Of Religion | 1.56 | Lib
 |  | Establishment Of Religion | 2 | Lib
 |  | Total | 1.78 | Lib
Sgbreyer | First Amendment | Free Exercise Of Religion | 1.78 | Lib
 |  | Establishment Of Religion | 1.67 | Lib
 |  | Total | 1.72 | Lib
Jgroberts | First Amendment | Free Exercise Of Religion | 2 | Lib
 |  | Establishment Of Religion | 1 | Cons.
 |  | Total | 1.78 | Lib.
Saalito | First Amendment | Free Exercise Of Religion | 2 | Lib.
 |  | Establishment Of Religion | 1 | Cons.
 |  | Total | 1.75 | Lib.
Ssotomayor | First Amendment | Free Exercise Of Religion | 1.5 | Lib/Con
 |  | Establishment Of Religion | 2 | Lib.
 |  | Total | 1.63 | Lib.
Ekagan | First Amendment | Free Exercise Of Religion | 1.8 | Lib.
 |  | Establishment Of Religion | 2 | Lib.
 |  | Total | 1.83 | Lib.
Nmgorsuch | First Amendment | Free Exercise Of Religion | 2 | Lib.
 |  | Total | 2 | Lib.
Total | First Amendment | Free Exercise Of Religion | 1.78 | Lib.
 |  | Establishment Of Religion | 1.46 | Cons.
 |  | Total | 1.65 | Lib.



### Prediction Summary


The general ideological value scores predict a 5-4 split along the usual lines (figure 5 include a ref).  The conservative majority coalition consists of Justices, Kennedy, Thomas, Roberts, Alito, and Gorsuch.  The liberal minority is of Justices Ginsberg, Breyer, Sotomayor, and Kagan.  

	
The ideological scores by the first amendment issue area, predicts a very different outcome.  For instance, a 7-2 liberal majority is expected.  Kennedy, is expected to vote with the conservative coalition, along with Gorsuch.  The Liberal majority consists of, Thomas, Ginsberg, Breyer, Roberts, Alito, Sotomayor, and Kagan.  


Testing again for individual issue areas, the results seem spurious.  When controlling for just the establishment clause, there is a 5-4 majority conservative coalition comprised of Justices Kennedy, Thomas, Roberts, Alito and Gorsuch.  The minority coalition consists of Justices, Ginsberg, Breyer, Sotomayor, Kagan.  However, when controlling for Free Exercise, a 9-0 liberal majority is the expected outcome.  


## Findings

### Actual Results

The actual results of Masterpiece Cakeshop, Ltd, v. Chicago Civil Rights Commission (2018) yield a 7-2 conservative majority in favor of Mr. Phillips consisting of Justice Roberts, Justice Kennedy, Justice Thomas, Justice Breyer, Justice Alito, Justice Kagan, and Justice Gorsuch.  The liberal minority consist of Justice Ginsberg and Justice Sotomayor.  Justice Kennedy delivered the opinion of the Court. 
	
The set of ideological values that best predict the actual outcome of the case is the general ideological score.  A 5-4 conservative majority in this case was expected with Justices Kennedy, Thomas, Roberts, Alito, and Gorsuch in the majority.  Justices Ginsberg, Breyer, Sotomayor, and Kagan were in the expected minority.  

### Attitudinal Model Evaluation

The discrepancy between the expected results and the actual results is difficult to explain.  Restricting the analysis at this point to only the attitudinal model the explanation must be that the ideologies of the justices acted upon the facts of the case, the situations in an unexpected way.  This could be caused by two factors. The first being that the variables defining conservatism and liberalism are inaccurate.  The other being that Justices, primarily the liberals which voted conservatively voted against the dictate of their ideological preferences.  


As stated above the attributes defining liberalism are pro-civil liberties or civil rights, pro-underdog, anti-owner, anti-business, pro-government, pro-exercise of judicial action, and pro-judicial activism.  Justice Breyer and Justice Kagan both tend to vote towards this direction.  In Masterpiece Cakeshop Ltd, v. Colorado Civil Rights Commission (2018)  however, they did not.  To run through the facts of the case quickly, Mr. Phillips is the proprietor of a small business that discriminates against a quasi-suspect class of citizens (non-heterosexual couples) in violation of Colorado state civil rights law.  When brought to suit, a civil rights administration of the state of Colorado, which is de-facto a quasi-judicial bureaucracy, oversaw the case and declared Mr. Phillip in violation of generally applicable and religiously neutral Colorado public accommodation laws.  Or in other words, every factor leading to a liberal vote is apparent in this case.  So then, Justices’ Breyer and Kagan moving in the conservative direction is remarkable.  


Or is it?   While reading through the Court’s opinion, the Court does not greatly address Mr. Phillips’ claim.  In fact, Justice Kennedy completely side steps the freedom of speech and religious freedom haymaker.  Rather, the object of consideration turns from Mr. Phillip’s to the actions of the state’s Civil Rights Commission.  “When the Colorado Civil Rights Commission considered this case, it did not do so with the religious neutrality that the Constitution requires.” (Masterpiece Cakeshop Ltd. v. Colorado Civil Rights Commission 2018) Considering this change in object, is it that the pertinent facts of the case change as well? 

Pro-civil liberties or civil rights, pro-underdog, anti-owner, anti-business, pro-government, pro-exercise of judicial action, and pro-judicial activism all still apply.  With the additional imposition by the Commission of “comprehensive staff training” and “quarterly compliance reports” it could also be argued that the pro-affirmative action factor may be active in this case. However, the startling material fact that distinguishes this case is the abject hostility the Civil Rights Commission demonstrated towards Mr. Philips’ “sincerely held religious beliefs (Masterpiece Cakeshop Ltd. v. Colorado Civil Rights Commission 2018).”  Therefore, the pro-neutrality of the establishment clause is grossly violated.  To such a degree that the “clear and impermissible hostility towards [the] sincere religious beliefs (Masterpiece Cakeshop Ltd. v. Colorado Civil Rights Commission 2018)” forced two liberal Justices to join the conservative coalition.  

In Justice Kagan’s own words, 


> “[I]t is a general rule that [religious and philosophical] objections do not allow business owners and other actors in the economy and in society to deny protected persons equal access to goods and services under a neutral and generally applicable public accommodations law.” Ante, at 9. But in upholding that principle, state actors cannot show hostility to religious views; rather, they must give those views “neutral and respectful consideration.” Ante, at 12. I join the Court’s opinion in full because I believe the Colorado Civil Rights Commission did not satisfy that obligation. (Masterpiece Cakeshop Ltd. v. Colorado Civil Rights Commission 2018)


What is apparent then is that Justice Kagan recognizes that in order to apply the establishment clause neutrally the federal and state governments must not act with hostility towards individuals with sincerely held religious beliefs.  Laws of general applicability in order to be constitutional must not unduly harm religious individuals.  Thus, Justice Breyer, and Justice Kagan both agree in full with the opinion of the Court.  

### Legal Model Evalution

More startling then the actual outcome of the case is the fact that the Justices largely adhered to precedent, or at least to the judicially created rule that valid law applied neutrally in respect to the establishment clause may be considered good law.  When considering the facts of the case to previous first amendment questions the results in light of the Civil Rights Commission’s hostility towards Mr. Phillips are not in any way remarkable.  

The three-pronged Lemon v. Kurtzman (1971) test exclusively could yield the same results.  First the Colorado law does have a secular purpose.  On the other hand, due to the way in which the Civil Rights Commission applied the law, its effect “inhibits religion”.  Because of that inhibition, the Colorado state government does become unnecessarily entangled in religion.  Passing through the matrix, the actions of the state are obviously unconstitutional.  

Consulting also Employment Div. v. Smith (1990) the court in Masterpiece Cakeshop Ltd, v. Colorado Civil Rights Commission (2018) stuck to their statement that “it is a permissible reading of U.S Const. Amend. I to say that if prohibiting the exercise or religion is not the object of a law, but merely the incidental effect of a generally applicable and otherwise valid provision, the First Amendment has not been offended (Employment Div. v. Smith, 1990).”  Therefore, a law of general applicability, applied neutrally does not warrant individual exemptions.  A point driven home by Justice Kennedy in the majority opinion, and also by Justice Kagan in her concurrence.  


Also echoed is the basic reasoning of Obergefell v. Hodges (2015) that “under the Due Process and Equal Protections Clauses of the Fourteenth Amendment couples of the same-sex may not be deprived” of their right to marry and to share the same privileges of same-sex couples.


The cynical critique, however of the Court’s adherence to precedent is the fact that to a large degree precedent does not conflict with the ideological preferences of the members of the Court.   Many of the cases cited by Justice Kennedy he either authored or was member to the majority.  To those that he was not, the opinions may be linked to ideological predecessors. 


Justice Kagan and Justice Breyer most likely voted “conservatively” due to the fact that the outcome of the case supports well established liberal precedent.  Namely in support of the neutrality of the establishment clause.  The opinion may have also persuaded their vote.  In it Justice Kennedy supports the validity of public accommodation laws protecting the civil rights of same-sex couples and people of other sexual orientations.   In the words of the Court, “It is unexceptional that Colorado law can protect gay persons, just as it can protect other classes of individuals, in acquiring whatever products and services they choose on the same terms and conditions as are offered to other members of the public (Masterpiece Cakeshop v. Colorado Civil Rights Commission, 2018)”.  It is my hypothesis that due the fact that this provision, which supports the basis of the Colorado Public Accommodation law, and the opinion in general supports a neutral application of the Establishment Clause, two liberal Justices voted in the conservative majority. 


[^need]: Include a reference!
[^reference]: Include a reference to the definition.
[^const]: Include reference to constitutional ammendment and clause
[^expand]:  This sentence doesn't really mean anything.  Expand upon it.  
[^claim]: reference his claim
[^laws]:  Georgia Laws, p 16; Massachusetts Perpetual laws, p. 7; New Hampshire Laws, pp. 26, 27; North Carolina Laws, p. 275.  
[^laws2]:  North Carolina Laws, p. 280; Massachusetts Perpetual Laws, pp. 5-6, New Hampshire Laws, p. 23;  South Carolina Laws, App., p. 41; Virginia Religious Freedom Act, pp. 7. 
[^symbolic-speech]:  An argument could be made that language is inherently symbolic speech, but references to contemporary works must be support the argument.   The intent behind the amendment does not seem to apply to the public exhibition of painting and sculpture.

[^impossible]:  Again, it is impossible to actually determine original intent.
[^william-and-mary]: This clause importantly was written in response to the Catholic persecution of English Protestants under the reign of King James.  Under William and Mary, following the Glorious Revolution, the English Bill of Rights limited the discretion of the monarch, and secured the prevalence of the Parliament.

[^tradition]:  Traditional is to be understood as a heterosexual relationship of members of the same race.  Nontraditional is to be anything that differs from that idea. 