from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from math import ceil
from xvfbwrapper import Xvfb
from scraper import Scraper

Base = declarative_base()


class Comment(Base):
    __tablename__ = "comments"

    uscisid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    comment = Column(String, nullable=False)
    date_posted = Column(String, nullable=False)
    date_received = Column(String, nullable=False)
    traking_number = Column(String, nullable=False)
    rin = Column(String, nullable=False)


if __name__ == "__main__":

    engine = create_engine('sqlite:///comments.sqlite')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance.
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Start virtual display.
    vdisplay = Xvfb()
    vdisplay.start()

    # Start scraper.
    scraper = Scraper(delay=4)

    # Get the total number of comments.
    total_comments = scraper.get_comments_total()
    total_pages = ceil(total_comments / 50)  # 50 comments per page.

    # Go through all pages.
    for page in range(1, total_pages + 1):
        # Get comment urls on given page.
        urls = scraper.get_comments_urls_on_page(page)

        for i, url in enumerate(urls):
            # USCIS ID.
            uscisid = url.split("=")[-1]

            # Check if entry exists.
            exists = session.query(Comment).filter(
                Comment.uscisid == uscisid).first()
            if exists is None:
                c = scraper.scrape_comment(comment_url=url)

                try:
                    comment = Comment(
                        uscisid=uscisid,
                        name=c["name"],
                        comment=c["comment"],
                        date_posted=c["posted_date"],
                        date_received=c["received_date"],
                        traking_number=c["tracking_number"],
                        rin=c["rin"])
                    session.add(comment)
                    session.commit()
                    print(page, i, uscisid, c)
                except IntegrityError:  # Do not commit repeated comments.
                    session.rollback()

    scraper.shut_down()

    # Stop xvfb
    vdisplay.stop()
