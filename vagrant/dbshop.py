from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dirtbike_setup import Base, Manufacture, Bikes, User

engine = create_engine('sqlite:///dirtbike.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

User20 = User(name="Ryan Nichols", email="rnichols23@gmail.com", picture="https://lh3.googleusercontent.com/-h3HY7XJp4io/TZcXwJe7mGI/AAAAAAAAADw/wdg0BMkumBgHXCIDrd7JMji0FvpWBQX3wCEwYBhgL/w139-h140-p/CEO%2Bof%2BEntretales.jpg" )

# Manufactures for bikes 
manufacture1 = Manufacture(user_id=1, name="Yamaha")
session.add(manufacture1)
session.commit()

manufacture2 = Manufacture(user_id=1, name="Honda")
session.add(manufacture2)
session.commit()

manufacture3 = Manufacture(user_id=1, name="Husqvarna")
session.add(manufacture3)
session.commit()

manufacture4 = Manufacture(user_id=1, name="Kawasaki")
session.add(manufacture4)
session.commit()

manufacture5 = Manufacture(user_id=1, name="KTM")
session.add(manufacture5)
session.commit()

manufacture6 = Manufacture(user_id=1, name="Suzuki")
session.add(manufacture6)
session.commit()


# Yamaha Bikes
kiddie = Bikes(user_id=1, name="Yamaha", description="fast bike",
                     price="$900.00", size="65cc", manufacture=manufacture1)

session.add(kiddie)
session.commit()

youth = Bikes(user_id=1, name="Yamaha", description="fast bike",
                     price="$1100.00", size="80cc", manufacture=manufacture1)

session.add(youth)
session.commit()

adult = Bikes(user_id=1, name="Yamaha", description="fast bike",
                     price="$1600.00", size="125cc", manufacture=manufacture1)

session.add(adult)
session.commit()

expert = Bikes(user_id=1, name="Yamaha", description="fast bike",
                     price="$2600.00", size="250cc", manufacture=manufacture1)

session.add(expert)
session.commit()

# Honda Bikes
kiddie = Bikes(user_id=1, name="Honda", description="fast bike",
                     price="$900.00", size="65cc", manufacture=manufacture2)

session.add(kiddie)
session.commit()

youth = Bikes(user_id=1, name="Honda", description="fast bike",
                     price="$1100.00", size="80cc", manufacture=manufacture2)

session.add(youth)
session.commit()

adult = Bikes(user_id=1, name="Honda", description="fast bike",
                     price="$1600.00", size="125cc", manufacture=manufacture2)

session.add(adult)
session.commit()

expert = Bikes(user_id=1, name="Honda", description="fast bike",
                     price="$2600.00", size="250cc", manufacture=manufacture2)

session.add(expert)
session.commit()

# Husqvarna Bikes
kiddie = Bikes(user_id=1, name="Husqvarna", description="fast bike",
                     price="$900.00", size="65cc", manufacture=manufacture3)

session.add(kiddie)
session.commit()

youth = Bikes(user_id=1, name="Husqvarna", description="fast bike",
                     price="$1100.00", size="80cc", manufacture=manufacture3)

session.add(youth)
session.commit()

adult = Bikes(user_id=1, name="Husqvarna", description="fast bike",
                     price="$1600.00", size="125cc", manufacture=manufacture3)

session.add(adult)
session.commit()

expert = Bikes(user_id=1, name="Husqvarna", description="fast bike",
                     price="$2600.00", size="250cc", manufacture=manufacture3)

session.add(expert)
session.commit()


# Kawasaki Bikes
kiddie = Bikes(user_id=1, name="Kawasaki", description="fast bike",
                     price="$900.00", size="65cc", manufacture=manufacture4)

session.add(kiddie)
session.commit()

youth = Bikes(user_id=1, name="Kawasaki", description="fast bike",
                     price="$1100.00", size="80cc", manufacture=manufacture4)

session.add(youth)
session.commit()

adult = Bikes(user_id=1, name="Kawasaki", description="fast bike",
                     price="$1600.00", size="125cc", manufacture=manufacture4)

session.add(adult)
session.commit()

expert = Bikes(user_id=1, name="Kawasaki", description="fast bike",
                     price="$2600.00", size="250cc", manufacture=manufacture4)

session.add(expert)
session.commit()


# KTM Bikes
kiddie = Bikes(user_id=1, name="KTM", description="fast bike",
                     price="$900.00", size="65cc", manufacture=manufacture5)

session.add(kiddie)
session.commit()

youth = Bikes(user_id=1, name="KTM", description="fast bike",
                     price="$1100.00", size="80cc", manufacture=manufacture5)

session.add(youth)
session.commit()

adult = Bikes(user_id=1, name="KTM", description="fast bike",
                     price="$1600.00", size="125cc", manufacture=manufacture5)

session.add(adult)
session.commit()

expert = Bikes(user_id=1, name="KTM", description="fast bike",
                     price="$2600.00", size="250cc", manufacture=manufacture5)

session.add(expert)
session.commit()

# Suzuki Bikes
kiddie = Bikes(user_id=1, name="Suzuki", description="fast bike",
                     price="$900.00", size="65cc", manufacture=manufacture6)

session.add(kiddie)
session.commit()

youth = Bikes(user_id=1, name="Suzuki", description="fast bike",
                     price="$1100.00", size="80cc", manufacture=manufacture6)

session.add(youth)
session.commit()

adult = Bikes(user_id=1, name="Suzuki", description="fast bike",
                     price="$1600.00", size="125cc", manufacture=manufacture6)

session.add(adult)
session.commit()

expert = Bikes(user_id=1, name="Suzuki", description="fast bike",
                     price="$2600.00", size="250cc", manufacture=manufacture6)

session.add(expert)
session.commit()

print "added menu items!"