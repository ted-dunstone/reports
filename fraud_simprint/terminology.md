# Terminology

## Glossary

Candidate
:   A sample from a gallery being compared against the probe.

\vskip 0.1 cm

Dataset
:   Is a collection of samples and metadata, such as person ids, images, age, gender etc.

\vskip 0.1 cm

Enrol
:   When a matcher is run against a sample to generate a template.

\vskip 0.1 cm

FTE
:   Failure to enrol

\vskip 0.1 cm

Gallery
:   A collection of templates, i.e all enrolled samples.

\vskip 0.1 cm

Ground Truth
:   Data which identifies genuine and imposter transactions (typically true or false, 1 or 0 etc.)

\vskip 0.1 cm

Match
:   A score created from the process of comparing two biometric samples acquired at different times from the same person.

\vskip 0.1 cm


Matcher
:   Is an implementation of an algorithm. Such algorithms could be face, voice and video recognition.

\vskip 0.1 cm

Modality
:   The matcher mode, ie face, voice or video.

\vskip 0.1 cm

Non-match
:   A score created from the process of comparing two biometric samples from the different people.

\vskip 0.1 cm


Probe
:   A sample or template to compare against the entire or subset of a gallery.

\vskip 0.1 cm

Results
:   A set of data scores relating to a dataset being run through a matcher.

\vskip 0.1 cm

Sample
:   The media file to process through the matcher, an image, video or audio clip.

\vskip 0.1 cm

Template
:   The sample after it has been enrolled by the matcher. The type of data is dependent on the algorithm used by the matcher.

\vskip 0.1 cm

False Reject Rate (FRR)
:   The proportion of genuine matches that are falsely non-matched (rejected). Also known as False Non-Match Rate .(FNMR)

\vskip 0.1 cm

False Accept Rate (FAR)
:   The proportion of imposter matches that are falsely matched (accepted). Also known as False Match Rate (FNMR).

\vskip 0.1 cm

Verification Rate
:   The proportion of verification attempts which are accepted. Commonly used for production data where no imposter ground truth is available.

\vskip 0.1 cm

Identification Rate
:   The proportion of genuine identification attempts for which the correct enrolment is returned in the candidate list.

## Plot Explainations

### 1.2 Zoo Plot

The zoo plot displays how different users perform based on their average match score and their average non-match score. Each point represents a single user and a good system will have few outliers. It can be used to investigate which users or user groups are causing more system errors when additional metadata is available.

**Data Required:** Biometric Scores, Ground Truth


In this example:

· **User A - _Worm_**

+ Average genuine score less than threshold (false rejection)

+ Average imposter score higher than threshold (false accept)

+ Worst possible users to have as they have difficulty verifying and are easily imposted

· **User B - _Chameleon_**

+ Average genuine score higher than threshold

+ Average imposter score higher than threshold

+ User may have very generic features weighted heavily by the algorithm

· **User C - _Phantom_**

+ Average genuine score less than threshold (false rejection)

+ Average imposter score less than threshold

+ Users may have very unique features and match poorly in all cases

· **User D - _Dove_**

+ Average genuine score higher than threshold

+ Average imposter score less than threshold

+ Best possible users to have as they verify easily and are more difficult to impost

### 1.3 ROC Curve

The Receive Operator Curve (ROC) curve shows the tradeoff between the rate of correct verification and chance of a false accept. A curve from a good system will be located near the top of the graph (high verification rate) for most false accept rates. The small bars show the confidence in the accuracy of the graph. For verification statistics, the ROC is commonly used to demonstrate accuracy and to compare systems.

**Data Required:** Biometric Scores, Ground Truth


In this example:

· **Point A – _Higher security setting_**

+ E.g. verification rate 85% at false accept rate 0.01%

+ Lower verification rate

+ Lower false accept rate

+ Decreased usability and increased security

· **Point B – _Lower security setting_**

+ E.g. verification rate 90% at false accept rate 0.05%

+ Higher verification rate

+ Higher false accept rate

+ Increased usability and decreased security

## 1.4 CMC Curve

The CMC curve displays the chance of a correct identification within the top ranked match results. A good system will start with a high identification rate for low ranks. The results in a CMC graph are highly dependent on the size of the database used for the test. The CMC curve can be used for identification system to answer questions such as “what is the chance of identifying a fraudster in the top 10 matches returned?”.