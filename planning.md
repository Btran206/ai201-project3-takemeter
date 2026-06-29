# Discourse Quality Classifier Plan

## 1) Task definition
My community that I chose is r/leagueoflegends because I play the game regularly and sometimes check this thread. This is a good fit for a classification task because posts can vary from highlights, discussion, and memes. In regards to discourse, the community can be very polarizing because there are varying levels of skill, which can offer opposing views. It's always fun to see other people's perspective on things which makes it interesting. My goal is to classify Reddit posts from r/leagueoflegends into labels that reflect how well the post contributes to respectful, useful discussion.

## 2) Labels
I will use four labels designed for top-level Reddit posts, not comment replies. Because my dataset consists of subreddit posts, the labels reflect what kinds of posts contribute meaningfully to the community versus what adds noise or harm at the post level.

### Label 1: Substantive Discussion
Definition: This label is for posts that make a specific claim, argument, or analysis about the game, meta, esports, or community with enough reasoning or evidence to invite real debate. The post does not need to be long, but it must take a position or offer an observation that others can meaningfully engage with.
- Example 1: "Top lane meta in pro play feels the most disconnected from average play — pro teams pick tankier utility champions while solo queue rewards carry-oriented builds, and the wave timing explains why."
- Example 2: "Aegis is too unbalanced in favor of non-priority roles because it scales better with gold-efficient farming patterns that supports and junglers can abuse more consistently."

### Label 2: Question or Help Request
Definition: This label is for posts that ask the community for advice, explanations, or opinions with enough context to get a useful answer. The post is seeking information rather than making an argument, but it is still a legitimate and specific contribution to the subreddit.
- Example 1: "Why was the Ryze rework dumbed down compared to the original spotlight? I noticed his kit used to have different mechanics and I am curious what drove that decision."
- Example 2: "Can any champion essentially become a tank if they build all tank items, or does base kit matter too much? Asking because I want to know if it works for my main."

### Label 3: Community or Entertainment Content
Definition: This label is for posts that share news, esports updates, art, humor, nostalgia, or gameplay highlights. These posts add social or entertainment value to the community but do not make an analytical argument or ask a specific gameplay question. They are not harmful, just not substantive discussion.
- Example 1: "Phantasm becomes the first ever player to hit 4000 LP" (news post with factual update)
- Example 2: "I miss Twisted Treeline — it was removed in 2019 and it was my favorite mode" (nostalgia post, community sentiment)
- Example 3: An art post or a meme that references a current patch or champion without making a gameplay argument.


## 3) Hard edge cases
The hardest cases will be posts where community value, tone, or scope make the label unclear.

### Likely ambiguous cases
- A nostalgia or opinion post with high upvotes but no specific argument — community signal suggests value, but the content is thin (Label 1 vs Label 3).
- A question post that also includes a strong opinion or argument in the body — the title reads as Label 2 but the body reads as Label 1.
- A complaint post that includes one specific, actionable point buried in a lot of venting — primary effect matters more than the isolated insight.
- An esports update post that also contains the author's analysis — pure news is Label 3, but added analysis may push it toward Label 1.
- A humor or meme post that is actually making a pointed critique of game balance — intent is entertainment but effect may be substantive.

### Annotation rule for ambiguous posts
If a post is genuinely split between two labels after reading the full title and body, I will annotate it using the label that best reflects the post's primary effect on the community.
If the ambiguity remains after discussion between annotators, I will mark the example as uncertain and exclude it from the main training set until a clear rule can be applied.

## 4) Data collection plan
I will collect posts from Reddit using the Reddit API on r/leagueoflegends and a mix of post types such as questions, advice, memes, and replies.

### Sampling strategy
- Pull examples from multiple threads and time periods rather than one single thread.
- Aim for about 300 labeled examples per class for the final dataset.
- Use a 70/15/15 split for training, validation, and test sets after labeling.

### If a label is underrepresented after 200 examples
I will not keep sampling randomly and hoping the balance fixes itself.
Instead, I will switch to targeted sampling by searching for posts that are likely to match the missing label, such as specific keywords, question patterns, or known discussion formats.
If a label still remains too small after that targeted effort, I will document the limitation and consider merging it with the closest related label only if the annotation guidelines clearly support that choice.

## 5) Evaluation metrics
Accuracy alone is not enough because the classes will likely be imbalanced and some mistakes matter more than others.

- Macro F1: this is the main metric because it gives each label equal importance and is better than raw accuracy when one class is more common.
- Per-label precision and recall: these are important because the model should not over-flag good posts or miss harmful ones.
- Confusion matrix: this helps show exactly which labels the model is confusing.

For a community moderation tool, false positives and false negatives have different costs, so a single accuracy score is too blunt.
A model that looks accurate overall but misses hostile posts would still be risky, and a model that over flags constructive posts would frustrate users.
The chosen metrics make those tradeoffs visible.

## 6) Definition of success
A classifier would be genuinely useful if it reaches strong performance on held-out data and clearly separates the most important categories.

### Useful performance target
- Macro F1 of at least 0.80 on the test set.
- Precision and recall of at least 0.80 for the two most important labels: Constructive and Hostile.
- A confusion matrix that shows most mistakes happen between nearby categories such as Clarifying and Constructive, not between Constructive and Hostile.

### Good enough for a real community tool
I would consider the system good enough for deployment as a support tool if it reaches a macro F1 of about 0.75 or higher and is reliable enough for human reviewers to trust its top predictions.
That would mean the model is not perfect, but it is strong enough to help prioritize posts for review rather than make final moderation decisions on its own.

## 7) Honest error analysis plan
After the first model run, I will inspect the worst mistakes manually.
This will show whether the model is failing because of wording, context, sarcasm, or annotation inconsistency.
That analysis is just as important as the numeric score because it reveals where the system actually works and where it still needs improvement.
