from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class DomainRecords(Base):
    __tablename__ = "domain_records"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ipv4 = relationship("IpV4Records", back_populates="domain")
    ipv6 = relationship("IpV6Records", back_populates="domain")


class IpV4Records(Base):
    __tablename__ = "ipv4_records"

    id = Column(Integer, primary_key=True, index=True)
    ip_string = Column(String)
    domain_id = Column(Integer, ForeignKey("domain_records.id"))
    domain = relationship("DomainRecords", back_populates="ipv4")


class IpV6Records(Base):
    __tablename__ = "ipv6_records"

    id = Column(Integer, primary_key=True, index=True)
    ip_string = Column(String)
    domain_id = Column(Integer, ForeignKey("domain_records.id"))
    domain = relationship("DomainRecords", back_populates="ipv6")
