CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    Date DATE,
    Amount INT,
    Description NVARCHAR(100)
);

INSERT INTO Transactions VALUES
(201, '2026-10-01', 5000, 'Payment from Client A'),
(202, '2026-10-02', 3000, 'Payment from Client B'),
(203, '2026-10-03', 7000, 'Payment from Client C'),
(204, '2026-10-04', 4500, 'Payment from Client D'),
(205, '2026-10-05', 6000, 'Payment from Client E'),
(206, '2026-10-06', 3200, 'Payment from Client F'),
(207, '2026-10-07', 2800, 'Payment from Client G'),
(211, '2026-10-08', 5100, 'Payment from Client H'), -- mismatch: ID 211 vs 208
(209, '2026-10-09', 4000, 'Payment from Client I'),
(212, '2026-10-10', 3600, 'Payment from Client J'); -- mismatch: ID 212 vs 210, amount differs
