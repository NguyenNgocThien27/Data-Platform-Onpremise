from pyspark.sql.types import *

mysql_Info = StructType([
    StructField("id", LongType(), True),
    StructField("name", StringType(), True),
    StructField("address", StringType(), True),
    StructField("datetime", TimestampType(), True),
    StructField("amount", DoubleType(), True)
])

mysql_Users = StructType([
    StructField('user_id', IntegerType(), False),
    StructField('username', StringType(), False),
    StructField('email', StringType(), False),
    StructField('age', IntegerType(), False),
    StructField('country', StringType(), False),
    StructField('transaction', StringType(), False),
    StructField('timestamp', StringType(), False)])

mongodb_Resident_Info = StructType([
    StructField("userId", StringType(), nullable=True),
    StructField("Action", StringType(), nullable=True),
    StructField("Address", StringType(), nullable=True),
    StructField("Apartments", ArrayType(StructType([
        StructField("block", StringType(), nullable=True),
        StructField("role", StringType(), nullable=True),
        StructField("floor", StringType(), nullable=True),
        StructField("room", StringType(), nullable=True)
    ])), nullable=True),
    StructField("ApprovedTime", StringType(), nullable=True),
    StructField("Approver", StringType(), nullable=True),
    StructField("ApproverEmail", StringType(), nullable=True),
    StructField("ApproveStatus", StringType(), nullable=True),
    StructField("AuthyID", StringType(), nullable=True),
    StructField("Avatar", StringType(), nullable=True),
    StructField("badgeId", StringType(), nullable=True),
    StructField("Birthday", StringType(), nullable=True),
    StructField("Career", StringType(), nullable=True),
    StructField("CMND", StringType(), nullable=True),
    StructField("CMNDNote", StringType(), nullable=True),
    StructField("CreatedTime", StringType(), nullable=True),
    StructField("District", StringType(), nullable=True),
    StructField("Email", StringType(), nullable=True),
    StructField("FaceID", ArrayType(StringType(), containsNull=True), nullable=True),
    StructField("FullName", StringType(), nullable=True),
    StructField("isAddedUnified", BooleanType(), nullable=True),
    StructField("isReceiveNotification", BooleanType(), nullable=True),
    StructField("isStaff", BooleanType(), nullable=True),
    StructField("IssueDate", StringType(), nullable=True),
    StructField("IssuePlace", StringType(), nullable=True),
    StructField("Nationality", StringType(), nullable=True),
    StructField("Note", StringType(), nullable=True),
    StructField("Password", StringType(), nullable=True),
    StructField("Phone", StringType(), nullable=True),
    StructField("Province", StringType(), nullable=True),
    StructField("reason", StringType(), nullable=True),
    StructField("RegistrationType", StringType(), nullable=True),
    StructField("ResidenceStatus", StringType(), nullable=True),
    StructField("Sex", StringType(), nullable=True),
    StructField("SubAccount", BooleanType(), nullable=True),
    StructField("Username", StringType(), nullable=True),
    StructField("Ward", StringType(), nullable=True)
])
