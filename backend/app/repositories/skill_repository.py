from sqlalchemy.orm import Session

from app.models.skill import Skill


def get_or_create_many(db: Session, names: list[str]) -> list[Skill]:
    if not names:
        return []
    existing = db.query(Skill).filter(Skill.name.in_(names)).all()  # one query for all names
    by_name = {skill.name: skill for skill in existing}
    for name in names:
        if name not in by_name:
            by_name[name] = Skill(name=name)
            db.add(by_name[name])
    return [by_name[name] for name in names]