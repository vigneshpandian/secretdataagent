CREATE TABLE IF NOT EXISTS public.secrettransactions
(
    "PartitionKey" text COLLATE pg_catalog."default",
    "RowKey" text COLLATE pg_catalog."default",
    "CategoryName" text COLLATE pg_catalog."default",
    "CreatedDate" timestamp with time zone,
    "Email" text COLLATE pg_catalog."default",
    "FirstName" text COLLATE pg_catalog."default",
    "IsDeleted" boolean,
    "LastName" text COLLATE pg_catalog."default",
    "LedgerId" text COLLATE pg_catalog."default",
    "LedgerType" text COLLATE pg_catalog."default",
    "ModifiedDate" timestamp with time zone,
    "TransactionAmount" numeric(18,2),
    "TransactionDate" timestamp with time zone,
    "TransactionNotes" text COLLATE pg_catalog."default",
    "GoldWeight" numeric(18,3),
    "IsCreditCardTransaction" boolean,
    "EmailBody" text COLLATE pg_catalog."default",
    "EmailId" text COLLATE pg_catalog."default",
    "SenderEmailId" text COLLATE pg_catalog."default",
    "Status" text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public.secrettransactions
    OWNER to postgres;


INSERT INTO SecretTransactions (
    PartitionKey,
    RowKey,
    CategoryName,
    CreatedDate,
    Email,
    FirstName,
    IsDeleted,
    LastName,
    LedgerId,
    LedgerType,
    ModifiedDate,
    TransactionAmount,
    TransactionDate,
    TransactionNotes,
    GoldWeight,
    IsCreditCardTransaction,
    EmailBody,
    EmailId,
    SenderEmailId,
    Status
) VALUES
('May-2020', '3a12d496-8be3-4e91-b8df-5ab1f1e9e921', 'Dining', '2020-05-03 09:42:18+00', 'arjun.mehta@gmail.com', 'Arjun', FALSE, 'Mehta', '3a12d496-8be3-4e91-b8df-5ab1f1e9e921', 'Expense', '2020-05-03 09:42:18+00', 845.00, '2020-05-02 19:15:00+00', 'Dinner with client at rooftop restaurant', NULL, TRUE, 'Hi Arjun, thanks for the meeting dinner. Please review the receipt.', 'e-1001', 'noreply@restaurant.com', 'Completed'),

('May-2020', '4db1d618-7ac2-49eb-a5c7-9d79f5022dff', 'Travel', '2020-05-10 18:11:44+00', 'priya.singh@yahoo.com', 'Priya', FALSE, 'Singh', '4db1d618-7ac2-49eb-a5c7-9d79f5022dff', 'Expense', '2020-05-10 18:11:44+00', 1430.50, '2020-05-09 08:30:00+00', 'Train ticket to Pune', NULL, TRUE, 'Your booking is confirmed for the train journey. Please keep the ticket handy.', 'e-1002', 'support@irctc.in', 'Approved'),

('Jun-2020', '5ef1234a-0f48-4383-9d23-8a0d71b8d4b6', 'Online gold', '2020-06-11 12:55:09+00', 'neha.das@outlook.com', 'Neha', FALSE, 'Das', '5ef1234a-0f48-4383-9d23-8a0d71b8d4b6', 'Expense', '2020-06-11 12:55:09+00', 250.00, '2020-06-10 17:00:00+00', 'Gold coin purchase', 10.00, FALSE, 'Your transaction for digital gold has been completed successfully.', 'e-1003', 'gold@paytm.com', 'Success'),

('Jun-2020', '6c0d770a-29a5-4d1d-80d0-9ae356f0c2ef', 'Pharmacy', '2020-06-18 08:20:55+00', 'rohan.verma@gmail.com', 'Rohan', FALSE, 'Verma', '6c0d770a-29a5-4d1d-80d0-9ae356f0c2ef', 'Expense', '2020-06-18 08:20:55+00', 186.75, '2020-06-17 14:20:00+00', 'Medicines and vitamins', NULL, TRUE, 'Prescription medicines purchased. Please consult your doctor if symptoms continue.', 'e-1004', 'care@medplus.com', 'Processed'),

('Jul-2020', '7ffb6d90-15b5-4a58-9b95-67ca7790cd12', 'Grocery', '2020-07-01 06:48:21+00', 'sofia.johnson@gmail.com', 'Sofia', FALSE, 'Johnson', '7ffb6d90-15b5-4a58-9b95-67ca7790cd12', 'Expense', '2020-07-01 06:48:21+00', 564.90, '2020-06-30 21:10:00+00', 'Weekly grocery order', NULL, FALSE, 'Your grocery order has been delivered. Please check the items before confirming.', 'e-1005', 'hello@bigbasket.com', 'Delivered'),

('Jul-2020', '8d725939-62c6-4d3d-89d0-8feb4d5c4f88', 'Electricity', '2020-07-08 09:30:02+00', 'kavya.nair@yahoo.com', 'Kavya', FALSE, 'Nair', '8d725939-62c6-4d3d-89d0-8feb4d5c4f88', 'Expense', '2020-07-08 09:30:02+00', 1320.00, '2020-07-07 20:45:00+00', 'Monthly electricity bill', NULL, TRUE, 'Bill payment successful for the electricity connection. Thank you.', 'e-1006', 'billing@powergrid.in', 'Paid'),

('Aug-2020', '9acaf07e-35a9-43de-81fa-3c0a8d4a57ef', 'Streaming', '2020-08-03 16:04:42+00', 'daniel.jacob@hotmail.com', 'Daniel', FALSE, 'Jacob', '9acaf07e-35a9-43de-81fa-3c0a8d4a57ef', 'Expense', '2020-08-03 16:04:42+00', 199.00, '2020-08-02 18:05:00+00', 'Netflix subscription renewal', NULL, TRUE, 'Your subscription has been renewed. Enjoy your plan.', 'e-1007', 'support@netflix.com', 'Active'),

('Aug-2020', 'aa33e98d-cd11-421d-9d34-6d0f7334ef6a', 'Food', '2020-08-15 13:50:11+00', 'meera.kapoor@gmail.com', 'Meera', FALSE, 'Kapoor', 'aa33e98d-cd11-421d-9d34-6d0f7334ef6a', 'Expense', '2020-08-15 13:50:11+00', 680.00, '2020-08-14 20:00:00+00', 'Biryani order', NULL, TRUE, 'Order placed successfully and out for delivery.', 'e-1008', 'delivery@swiggy.com', 'Delivered'),

('Sep-2020', 'bb74de2c-9bc6-44be-ba1a-1cb52ad2f647', 'Recharge', '2020-09-06 10:15:30+00', 'aisha.shaikh@live.com', 'Aisha', FALSE, 'Shaikh', 'bb74de2c-9bc6-44be-ba1a-1cb52ad2f647', 'Expense', '2020-09-06 10:15:30+00', 499.00, '2020-09-05 11:45:00+00', 'Mobile recharge', NULL, FALSE, 'Your mobile top-up has been processed successfully.', 'e-1009', 'support@airtel.in', 'Completed');