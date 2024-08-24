from itsdangerous import Serializer
from app.extensions import db, login_manager
from sqlalchemy import UniqueConstraint
# ... rest of the code remains the same

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User1(UserMixin, db.Model):
    __tablename__ = 'user1'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(10))  # 'debit' or 'credit'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),unique=True, nullable=False)
    session_id = db.Column(db.String(255), unique=True, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    txn_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    txn_amount = db.Column(db.Float, nullable=False)
    txn_type = db.Column(db.String(10), nullable=False)  # 'debit' or 'credit'

@login_manager.user_loader
def load_user(user_id):
    return User1.query.get(int(user_id))


#### Models from PMSPortal ########


class StructureMaster(db.Model):
    __tablename__ = "structure_master"
    id = db.Column(db.Integer, primary_key=True)
    structure_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime())

    # user = db.relationship('User', back_populates='amc_master')

    def __init__(self, structure_id, name, created_at):
        self.structure_id = structure_id
        self.name = name
        self.created_at = created_at


class CategoryMaster(db.Model):
    __tablename__ = "category_master"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime())

    # user = db.relationship('User', back_populates='amc_master')

    def __init__(self, category_id, name, created_at):
        self.category_id = category_id
        self.name = name
        self.created_at = created_at


class AMCMaster(db.Model):
    __tablename__ = "amc_master"
    id = db.Column(db.Integer, primary_key=True)
    amc_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime())

    # user = db.relationship('User', back_populates='amc_master')

    def __init__(self, amc_id, name, created_at):
        self.amc_id = amc_id
        self.name = name
        self.created_at = created_at


class IndexMaster(db.Model):
    __tablename__ = "index_master"

    id = db.Column(db.Integer, primary_key=True)
    index_ref = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    index_code = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime())

    def __init__(self, index_ref, name, index_code, created_at):
        self.index_ref = index_ref
        self.name = name
        self.index_code = index_code
        self.created_at = datetime.utcnow()


class StockMaster(db.Model):
    __tablename__ = "stock_master"

    id = db.Column(db.Integer, primary_key=True)
    stock_ref = db.Column(db.Integer)
    name = db.Column(db.String(30), nullable=False)
    stock_symbol = db.Column(db.String(50), nullable=False)
    isin_code = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime())

    def __init__(self, stock_ref, name, isin_code, stock_symbol, created_at):
        self.stock_ref = stock_ref
        self.name = name
        self.stock_symbol = stock_symbol
        self.isin_code = isin_code
        self.created_at = datetime.utcnow()


class SectorMaster(db.Model):
    __tablename__ = "sector_master"

    id = db.Column(db.Integer, primary_key=True)
    sector_ref = db.Column(db.Integer)
    name = db.Column(db.String(30), nullable=False)
    sector_code = db.Column(db.String(50))
    created_at = db.Column(db.DateTime())

    def __init__(self, sector_ref, name, sector_code, created_at):
        self.sector_ref = sector_ref
        self.name = name
        self.sector_code = sector_code
        self.created_at = datetime.utcnow()


class UserRole(db.Model):
    __tablename__ = "userrole"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    user = db.relationship("User", lazy="noload")

    def __init__(self, name, created_at):
        self.name = name
        self.created_at = created_at


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(250), nullable=False)
    userrole_id = db.Column(db.Integer(), db.ForeignKey("userrole.id"), nullable=False)
    amc_id = db.Column(db.Integer(), db.ForeignKey("amc_master.id"), nullable=True)
    isactive = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # thread = db.relationship('Thread', back_populates='user')

    def __init__(
        self,
        fname,
        lname,
        email,
        password,
        userrole_id,
        amc_id,
        isactive,
        created_at,
    ):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.userrole_id = userrole_id
        self.amc_id = amc_id
        self.isactive = isactive
        self.created_at = created_at
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    def get_token(self, expires_sec=300):
        serial = Serializer(secret_key="SERIALIZER_SECRET_KEY")
        return serial.dumps({"user_id": self.id})

    @staticmethod
    def verify_token(token):
        serial = Serializer(secret_key="SERIALIZER_SECRET_KEY")
        try:
            user_id = serial.loads(token, max_age=300)["user_id"]
        except:
            return None
        return User.query.get(user_id)


class TxnType(db.Model):
    __tablename__ = "txntype"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    def __init__(self, name, created_at):
        self.name = name
        self.created_at = created_at


class TxnLog(db.Model):
    __tablename__ = "txnlog"
    id = db.Column(db.Integer, primary_key=True)
    txntype_id = db.Column(db.Integer, db.ForeignKey("txntype.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=True)
    log_desc = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False)

    def __init__(self, txntype_id, log_desc, user_id, created_at):
        self.txntype_id = txntype_id

        self.user_id = user_id

        self.log_desc = log_desc
        self.created_at = datetime.utcnow()


class PMSMaster(db.Model):
    __tablename__ = "pms_master"
    id = db.Column(db.Integer, primary_key=True)
    pms_id = db.Column(db.Integer)
    amc_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    structure_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    index_id = db.Column(db.Integer, nullable=False)
    aum = db.Column(db.REAL, nullable=False)
    stocks_min = db.Column(db.Integer, nullable=False)
    stocks_max = db.Column(db.Integer, nullable=False)
    portfolio_pe = db.Column(db.REAL, nullable=False)
    large_cap = db.Column(db.REAL, nullable=False)
    mid_cap = db.Column(db.REAL, nullable=False)
    small_cap = db.Column(db.REAL, nullable=False)
    cash = db.Column(db.REAL, nullable=False)
    created_at = db.Column(db.DateTime())

    def __init__(
        self,
        pms_id,
        amc_id,
        category_id,
        structure_id,
        name,
        index_id,
        aum,
        stocks_min,
        stocks_max,
        portfolio_pe,
        large_cap,
        mid_cap,
        small_cap,
        cash,
        created_at,
    ):
        self.pms_id = pms_id
        self.amc_id = amc_id
        self.category_id = category_id
        self.structure_id = structure_id
        self.name = name
        self.index_id = index_id
        self.aum = aum
        self.stocks_min = stocks_min
        self.stocks_max = stocks_max
        self.portfolio_pe = portfolio_pe
        self.large_cap = large_cap
        self.mid_cap = mid_cap
        self.small_cap = small_cap
        self.cash = cash
        self.created_at = datetime.utcnow()


class PMSSector(db.Model):
    __tablename__ = "pms_sector"

    id = db.Column(db.Integer, primary_key=True)
    # strategy_id = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=False)
    pms_id = db.Column(db.Integer, nullable=False)
    sector_id = db.Column(db.Integer, nullable=False)
    pct_deployed = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime)

    # strategy = db.relationship('StrategyMaster', back_populates='sector_holdings')

    def __init__(self, pms_id, sector_id, pct_deployed, created_at):
        self.pms_id = pms_id
        self.sector_id = sector_id
        self.pct_deployed = pct_deployed
        self.created_at = datetime.utcnow()


class PMSNav(db.Model):
    __tablename__ = "pms_nav"

    id = db.Column(db.Integer, primary_key=True)
    # strategy_id = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=False)
    pms_id = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, nullable=False)
    p_month = db.Column(db.Integer, nullable=False)
    p_year = db.Column(db.Integer, nullable=False)
    nav = db.Column(db.Float, nullable=False)
    __table_args__ = (UniqueConstraint("pms_id", "p_month", "p_year"),)

    created_at = db.Column(db.DateTime)

    # strategy = db.relationship('StrategyMaster', back_populates='sector_holdings')

    def __init__(self, pms_id, user_id, p_month, p_year, nav, created_at):
        self.pms_id = pms_id
        self.user_id = user_id
        self.p_month = p_month
        self.p_year = p_year
        self.nav = nav
        self.created_at = datetime.utcnow()


class PMSStock(db.Model):
    __tablename__ = "pms_stock"

    id = db.Column(db.Integer, primary_key=True)
    # strategy_id = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=False)
    pms_id = db.Column(db.Integer, nullable=False)
    stock_id = db.Column(db.Integer, nullable=False)
    pct_deployed = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime)

    # strategy = db.relationship('StrategyMaster', back_populates='sector_holdings')

    def __init__(self, pms_id, stock_id, pct_deployed, created_at):
        self.pms_id = pms_id
        self.stock_id = stock_id
        self.pct_deployed = pct_deployed
        self.created_at = datetime.utcnow()


class PMSPerformance(db.Model):
    __tablename__ = "pms_performance"

    id = db.Column(db.Integer, primary_key=True)
    # amc_id = db.Column(db.Integer, db.ForeignKey('amc.id'))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pms_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    p_month = db.Column(db.Integer, nullable=False)
    p_year = db.Column(db.Integer, nullable=False)

    one_month = db.Column(db.Float)
    three_months = db.Column(db.Float)
    six_months = db.Column(db.Float)
    twelve_months = db.Column(db.Float)
    two_year_cagr = db.Column(db.Float)
    three_year_cagr = db.Column(db.Float)
    five_year_cagr = db.Column(db.Float)
    ten_year_cagr = db.Column(db.Float)
    cagr_si = db.Column(db.Float, nullable=False)
    si = db.Column(db.Float, nullable=False)

    __table_args__ = (UniqueConstraint("pms_id", "p_month", "p_year"),)
    # amc = db.relationship('AMC', back_populates='pms_performance')
    # user = db.relationship('User', back_populates='pms_performance')

    created_at = db.Column(db.DateTime)

    def __init__(
        self,
        pms_id,
        user_id,
        p_month,
        p_year,
        one_month,
        three_months,
        six_months,
        twelve_months,
        two_year_cagr,
        three_year_cagr,
        five_year_cagr,
        ten_year_cagr,
        cagr_si,
        si,
        created_at,
    ):
        self.pms_id = pms_id
        self.user_id = user_id
        self.p_month = p_month
        self.p_year = p_year
        self.one_month = one_month
        self.three_months = three_months
        self.six_months = six_months
        self.twelve_months = twelve_months
        self.two_year_cagr = two_year_cagr
        self.three_year_cagr = three_year_cagr
        self.five_year_cagr = five_year_cagr
        self.ten_year_cagr = ten_year_cagr
        self.cagr_si = cagr_si
        self.si = si

        self.created_at = datetime.utcnow()


class IndexPerformance(db.Model):
    __tablename__ = "index_performance"

    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id = db.Column(db.Integer, nullable=False)
    index_id = db.Column(db.Integer, nullable=False)
    p_month = db.Column(db.Integer, nullable=False)
    p_year = db.Column(db.Integer, nullable=False)

    one_month = db.Column(db.Float)
    three_months = db.Column(db.Float)
    six_months = db.Column(db.Float)
    twelve_months = db.Column(db.Float)
    two_year_cagr = db.Column(db.Float)
    three_year_cagr = db.Column(db.Float)
    five_year_cagr = db.Column(db.Float)
    ten_year_cagr = db.Column(db.Float)
    # cagr_si = db.Column(db.Float)
    created_at = db.Column(db.DateTime())

    # user = db.relationship('User', back_populates='pms_performance')

    __table_args__ = (UniqueConstraint("index_id", "p_month", "p_year"),)

    def __init__(
        self,
        user_id,
        index_id,
        p_month,
        p_year,
        one_month,
        three_months,
        six_months,
        twelve_months,
        two_year_cagr,
        three_year_cagr,
        five_year_cagr,
        ten_year_cagr,
        #  cagr_si,
        created_at,
    ):
        self.user_id = user_id
        self.index_id = index_id
        self.p_month = p_month
        self.p_year = p_year
        self.one_month = one_month
        self.three_months = three_months
        self.six_months = six_months
        self.twelve_months = twelve_months
        self.two_year_cagr = two_year_cagr
        self.three_year_cagr = three_year_cagr
        self.five_year_cagr = five_year_cagr
        self.ten_year_cagr = ten_year_cagr
        # self.cagr_si = cagr_si

        self.created_at = datetime.utcnow()

