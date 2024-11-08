# Treatment Assignment with oTree

This repository provides an implementation of treatment assignment functions based on quotas to ensure balanced participant distribution across different treatment groups in experimental sessions. The code supports multiple quota types (total, gender-based, and gender-age-based) and updates dynamically based on real-time participant data.
## Usage
- Add ```set_treatment.py``` to the project folder.
- Define ```DONE_TREATMENTS``` in ```settings.py``` and add it to ```SESSION_CONFIGS``` under the ```done_treatments``` key:
```python
# settings.py
DONE_TREATMENTS = {
    #'treatment': [female, male, non-binary]
    'treatment1': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    'treatment2': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    'treatment3': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
}

SESSION_CONFIGS = [
    dict(
        name='study1',
        display_name='Experiment',
        treatment_session=None,
        done_treatments=DONE_TREATMENTS,
    ),
]
```
- Define ```MAX_TREATMENTS1``` (or ```MAX_TREATMENTS2``` or ```MAX_TREATMENTS3```) in the ```C``` (Constants) class.
- Initialize ```done_treatments``` in the session variable:
```python
# __init__.py
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        subsession.session.done_treatments = subsession.session.config['done_treatments']
```
- Assign treatment (make sure to ask for age and gender beforehand, if required)
```python
# __init__.py
class Treatment(Page):

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.age = player.age
        player.participant.gender = player.gender
        player.participant.treatment = set_treatment(
            'gender_based', 
            player.subsession.session.done_treatments, 
            C.MAX_TREATMENTS2, 
            player.participant.gender, 
            player.participant.age
        )
```
- Update ```done_treatments``` after each participant completes the study:

```python
# __init__.py
class LastPage(Page):

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.subsession.session.done_treatments[player.participant.treatment][player.participant.gender][agecat(player.participant.age)] += 1
```

## Testing
Use ```test.py``` to test participant assignment to treatments.

## Help
If you have any questions, please feel free to contact me via my [homepage](https://www.studies-services.de/en).
