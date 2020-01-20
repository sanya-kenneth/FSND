from flask_sqlalchemy import SQLAlchemy
# from flask import current_app as app


db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            error=True
        finally:
            db.session.close()

    def edit(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            error=True
        finally:
            db.session.close()
            
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            error=True
        finally:
            db.session.close()


class Question(BaseModel):
    
    __tablename__ = 'question'

    question = db.Column(db.String, nullable=False, unique=True)
    teacher_id = db.Column(db.String(120))
    answer = db.relationship('Answer', backref='question', lazy=True)

    def format(self):
        result =  {
            "id": self.id,
            "question": self.question,
            "teacher_id": self.teacher_id}
        return result
    
    def __rep__(self):
        return f"<Question obj: {self.question}>"


class Answer(BaseModel):
    
    __tablename__ = 'answer'

    answer = db.Column(db.String, nullable=False, unique=True)
    student_id = db.Column(db.String(120))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    
    def format(self):
        result = {
            "id": self.id,
            "answer": self.answer
        }
        return result
    
    def __rep__(self):
        return f"<Answer obj: {self.answer}>"
