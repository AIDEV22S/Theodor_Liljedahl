from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
engine = create_engine('sqlite:///idrottsförening.db', echo=True)
base = declarative_base()
session = sessionmaker(bind=engine)()

class member(base):
    __tablename__ = "Member"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String)
    lastName = Column(String)
    adress = Column(String)
    postalNumber = Column(Integer)
    postalAdress = Column(String)
    feesPaid = Column(Boolean)

def createDatabase():
    base.metadata.create_all(engine)
def insertMember(newMember):
    session.add(newMember)
    session.commit()
def deleteMember(memberid):
    session.delete(session.query(member).filter(member.id == memberid).first())
    session.commit()
def getMemberAttributes(member):
    return [member.id,
            member.firstName,
            member.lastName,
            member.adress,
            member.postalNumber,
            member.postalAdress,
            member.feesPaid]
def getMemberList(): #returns all member attributes in a 2 dimensional list
    members = list(session.query(member))
    return list(map(getMemberAttributes, members))
def searchMembers(searchTerm, searchtype ):
    if searchtype == '-IDSEARCH-':
        return list(map(getMemberAttributes, session.query(member).filter(member.id == searchTerm)))
    if searchtype == '-FIRSTNAMESEARCH-':
        return list(map(getMemberAttributes, session.query(member).filter(member.firstName == searchTerm)))
    if searchtype == '-LASTNAMESEARCH-':
        return list(map(getMemberAttributes, session.query(member).filter(member.lastName == searchTerm)))
    if searchtype == '-ADRESSSEARCH-':
        return list(map(getMemberAttributes, session.query(member).filter(member.adress == searchTerm)))
    return []
def addSven():
    Sven = member(firstName='Sven', lastName='Ven', adress='Vengatan 12', postalNumber=23456, postalAdress='Vengatan', feesPaid=True)
    insertMember(Sven)