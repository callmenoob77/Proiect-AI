import enum
from sqlalchemy.types import Enum as SQLAlchemyEnum

class QuestionTypeEnum(enum.Enum):
    N_QUEENS = 'N_QUEENS'
    HANOI = 'HANOI'
    GRAPH_COLORING = 'GRAPH_COLORING'
    KNIGHT_TOUR = 'KNIGHT_TOUR'
    GAME_MATRIX = 'GAME_MATRIX'
    BACKTRACKING_ASSIGNMENT = 'BACKTRACKING_ASSIGNMENT'
    MINIMAX_TREE = 'MINIMAX_TREE'

class AnswerSourceEnum(enum.Enum):
    USER_UI = 'USER_UI'
    USER_PDF = 'USER_PDF'
    AGENT = 'AGENT'

QuestionTypeSQL = SQLAlchemyEnum(
    QuestionTypeEnum,
    name="question_type",
    create_type=False
)

AnswerSourceSQL = SQLAlchemyEnum(
    AnswerSourceEnum,
    name="answer_source",
    create_type=False
)