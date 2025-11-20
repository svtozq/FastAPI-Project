from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# -------------------- USER ACCOUNT --------------------
class UserAccount(Base):
    __tablename__ = "useraccount"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    date = Column(DateTime)

 # Relations
    bank_accounts = relationship("BankAccount", back_populates="user")
    beneficiaries = relationship("Beneficiary", back_populates="user")


# -------------------- BANK ACCOUNT --------------------
class BankAccount(Base):
    __tablename__ = "bankaccount"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("useraccount.id"), nullable=False)
    iban = Column(String(34), unique=True, nullable=False)
    balance = Column(Float, default=0)
    clotured = Column(Boolean, default=False)
    type= Column(String, default=False)
    BankAccount_date = Column(DateTime)

    # Relations
    user = relationship("UserAccount", back_populates="bank_accounts")
    beneficiaries = relationship("Beneficiary", back_populates="bank_account")
    sent_transactions = relationship("Transaction", foreign_keys="[Transaction.from_account_id]",
                                     back_populates="from_account")
    received_transactions = relationship("Transaction", foreign_keys="[Transaction.to_account_id]",
                                         back_populates="to_account")


# -------------------- BENEFICIARY --------------------
class Beneficiary(Base):
    __tablename__ = "beneficiary"

    id = Column(Integer, primary_key=True, index=True)
    bank_account_id = Column(Integer, ForeignKey("bankaccount.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("useraccount.id"), nullable=False)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    Beneficiary_date = Column(DateTime)

    # Relations
    bank_account = relationship("BankAccount", back_populates="beneficiaries")
    user = relationship("UserAccount", back_populates="beneficiaries")



# -------------------- TRANSACTION --------------------
class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    sender_last_name = Column(String(50), nullable=True)
    sender_first_name = Column(String(50), nullable=True)
    from_account_id = Column(Integer, ForeignKey("bankaccount.id"), nullable=False)
    to_account_id = Column(Integer, ForeignKey("bankaccount.id"), nullable=False)
    message = Column(String(255), nullable=True)
    date = Column(DateTime)
    balance = Column(Float, nullable=False)
    transaction_date = Column(DateTime)

    # Relations
    from_account = relationship("BankAccount", foreign_keys=[from_account_id], back_populates="sent_transactions")
    to_account = relationship("BankAccount", foreign_keys=[to_account_id], back_populates="received_transactions")