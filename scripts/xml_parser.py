from xml.sax import ContentHandler
from xml.sax import make_parser
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
import datetime
import os

XML_PARSE_FILE = os.getenv("XML_PARSE_FILE")
DATABASE_URL = os.getenv("DATABASE_PATH")

engine = create_engine(DATABASE_URL)
engine.connect()


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


class XmlHandler(ContentHandler):
    def __init__(self):
        self.current = None
        self.domain = None
        self.domain_obj = None
        self.count_object = 0
        self.ipv4_array = []
        self.ipv6_array = []
        self.ipv6 = None
        self.ipv4 = None

    def startElement(self, name, attrs):
        self.current = name

        if name == "content":
            print("\n\n//////////////////////////////////////////////")
            print(f"             CONTENT -- [{attrs['id']}]")
            print("//////////////////////////////////////////////")

    def characters(self, content):
        if self.current == "domain":
            self.domain = content
            self.count_object += 1
            print(content)
        if self.current == "ip":
            self.ipv4 = content
            self.count_object += 1
            print(content)
        if self.current == "ipv6":
            self.ipv6 = content
            self.count_object += 1
            print(content)

    def endElement(self, name):
        if self.current == "domain":
            self.domain_obj = DomainRecords(name=self.domain)
        if self.current == "ip":
            self.ipv4_array.append(IpV4Records(ip_string=self.ipv4))
        if self.current == "ipv6":
            self.ipv6_array.append(IpV6Records(ip_string=self.ipv6))

        if name == "content":
            if self.domain_obj:
                self.domain_obj.ipv4 = self.ipv4_array
                self.domain_obj.ipv6 = self.ipv6_array

                with Session(bind=engine) as session:
                    session.add(self.domain_obj)
                    session.commit()

            self.current = None
            self.domain = None
            self.domain_obj = None
            self.ipv4_array = []
            self.ipv6_array = []
            self.ipv6 = None
            self.ipv4 = None


def start_parsing_file():
    handler = XmlHandler()
    parser = make_parser()
    parser.setContentHandler(handler)

    parser.parse(XML_PARSE_FILE)


if __name__ == "__main__":
    if input("create a table in the database?(y/n)") == "y":
        Base.metadata.create_all(bind=engine)

    if input("run the parser?(y/n)") == "y":
        start_time = datetime.datetime.now()
        start_parsing_file()
        print(datetime.datetime.now() - start_time)
