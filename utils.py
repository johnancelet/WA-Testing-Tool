import logging
import csv

UTF_8 = 'utf-8'
TRAIN_FILENAME = 'train.csv'
TEST_FILENAME = 'test.csv'
TEST_OUT_FILENAME = 'test-out.csv'

INTENT_COLUMN = 'intent'
CONFIDENCE_COLUMN = 'confidence'
UTTERANCE_COLUMN = 'utterance'  # used in any intermediate file
INTENT_JUDGE_COLUMN = 'does intent match'
PREDICTED_INTENT_COLUMN = 'predicted intent'
DETECTED_ENTITY_COLUMN = 'detected entity'
DIALOG_RESPONSE_COLUMN = 'dialog response'
GOLDEN_INTENT_COLUMN = 'golden intent'

FOLD_NUM_DEFAULT = '5'
WCS_VERSION = '2018-02-16'
WORKSPACE_ID_TAG = 'workspace_id'
TIME_TO_WAIT = 600


logger = logging.getLogger(__name__)


def configure_logger(level, format):
    """ Styling the logs in each module
    """
    logger.setLevel(level)
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter(format))
    logger.addHandler(h)


def save_dataframe_as_csv(df, file):
    """ Save dataframe as csv
    """
    return df.to_csv(file, encoding=UTF_8, quoting=csv.QUOTE_ALL,
                     index=False)


def marshall_entity(entities):
    """ Serialize RuntimeEntity list into formatted string
    """
    return ';'.join(['{}:{}'.format(entity['entity'], entity['value'])
                     for entity in entities])


def unmarshall_entity(entities_str):
    """ Deserialize entities string to RuntimeEntity list
    """
    entities = []
    for entity_str in entities_str.split(';'):
        splitted = entity_str.split(':')
        entities.append({'entity': splitted[0], 'value': splitted[0]})
    return entities