## happy path
* greet
  - utter_greet
* faq
    - respond_faq
    - action_set_faq_slot
* mood_great
  - utter_happy


## FAQ
* faq
    - respond_faq
    - action_set_faq_slot
* mood_great
  - utter_happy

## happy path query number
* greet
  - utter_greet
* faq
    - respond_faq
    - action_set_faq_slot
* query_numbers
  - form_reply_number
  - form {"name": "form_reply_number"}
  - form {"name": null}
* faq
    - respond_faq
    - action_set_faq_slot


## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy
* faq
    - respond_faq
    - action_set_faq_slot

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* faq
    - respond_faq
    - action_set_faq_slot
* deny
  - utter_goodbye

## say goodbye
* faq
    - respond_faq
    - action_set_faq_slot
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
