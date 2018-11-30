from .. import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    rate = db.Column(db.Float)
    release = db.Column(db.Integer)
    img = db.Column(db.String(64))

    @staticmethod
    def generate_fake(count=100):
        from random import seed
        from random import randint
        import forgery_py

        seed()
        for i in range(count):
            m = Movie(title=forgery_py.lorem_ipsum.title(),
                      rate=randint(0, 50)/10,
                      release=randint(2000, 2019),
                      img=forgery_py.internet.domain_name())
            db.session.add(m)
            try:
                db.session.commit()
            except:
                db.session.rollback()

