"use client";

import { useState } from "react";

interface Person {
    name: string;
    qr: File | null;
}

interface Expense {
    id: number;
    name: string;
    amount: number;
    paidBy: string;
    category: string;
    note: string;
    createdAt: string;
}

interface Settlement {
    id: number;
    from: string;
    to: string;
    amount: number;
    completedAt?: string;
}

export default function ExpenseCard() {
    const totalBudget = 25000;

    const [peopleCount, setPeopleCount] = useState(0);
    const [people, setPeople] = useState<Person[]>([]);

    const [expenseName, setExpenseName] = useState("");
    const [amount, setAmount] = useState("");
    const [paidBy, setPaidBy] = useState("");
    const [category, setCategory] = useState("Food");
    const [note, setNote] = useState("");

    const [expenses, setExpenses] = useState<Expense[]>([]);
    const [completedExpenses, setCompletedExpenses] = useState<Expense[]>([]);
    const [settlementHistory, setSettlementHistory] = useState<Settlement[]>([]);
    const [completedSettlementIds, setCompletedSettlementIds] = useState<number[]>([]);

    const inputStyle =
        "w-full border border-gray-200 focus:ring-2 focus:ring-purple-400 outline-none p-3 rounded-2xl";

    const cardStyle =
        "bg-white rounded-3xl shadow-md border border-gray-100";

    // ---------------- GROUP ----------------
    const handlePeopleCount = (count: number) => {
        setPeopleCount(count);

        const newPeople = Array.from({ length: count }, (_, i) => ({
            name: people[i]?.name || "",
            qr: people[i]?.qr || null,
        }));

        setPeople(newPeople);
    };

    const handlePersonName = (index: number, value: string) => {
        const updated = [...people];
        updated[index].name = value;
        setPeople(updated);
    };

    const handleQRUpload = (index: number, file: File) => {
        const updated = [...people];
        updated[index].qr = file;
        setPeople(updated);
    };

    // ---------------- ADD EXPENSE ----------------
    const addExpense = () => {
        if (!expenseName || !amount || !paidBy) {
            alert("Fill all fields");
            return;
        }

        const newExpense: Expense = {
            id: Date.now(),
            name: expenseName,
            amount: Number(amount),
            paidBy,
            category,
            note,
            createdAt: new Date().toLocaleString(),
        };

        setExpenses([...expenses, newExpense]);

        setExpenseName("");
        setAmount("");
        setPaidBy("");
        setCategory("Food");
        setNote("");
    };

    const markExpensePaid = (id: number) => {
        const expense = expenses.find((e) => e.id === id);
        if (!expense) return;

        setCompletedExpenses([...completedExpenses, expense]);
        setExpenses(expenses.filter((e) => e.id !== id));
    };

    // ---------------- TOTAL ----------------
    const totalSpent = [...expenses, ...completedExpenses].reduce(
        (acc, item) => acc + item.amount,
        0
    );

    const remaining = totalBudget - totalSpent;

    // ---------------- CATEGORY ----------------
    const categoryTotals = [...expenses, ...completedExpenses].reduce(
        (acc: any, item) => {
            acc[item.category] = (acc[item.category] || 0) + item.amount;
            return acc;
        },
        {}
    );

    // ---------------- SPLIT ----------------
    const generateSettlements = () => {
        if (people.length === 0 || totalSpent === 0) return [];

        const perPerson = totalSpent / people.length;
        const paidMap: any = {};

        people.forEach((person) => {
            paidMap[person.name] = 0;
        });

        [...expenses, ...completedExpenses].forEach((expense) => {
            paidMap[expense.paidBy] += expense.amount;
        });

        const creditors: any[] = [];
        const debtors: any[] = [];

        Object.keys(paidMap).forEach((person) => {
            const diff = paidMap[person] - perPerson;

            if (diff > 0) {
                creditors.push({
                    name: person,
                    amount: diff,
                });
            }

            if (diff < 0) {
                debtors.push({
                    name: person,
                    amount: Math.abs(diff),
                });
            }
        });

        const settlements: Settlement[] = [];

        debtors.forEach((debtor) => {
            creditors.forEach((creditor) => {
                if (debtor.amount > 0 && creditor.amount > 0) {
                    const payAmount = Math.min(
                        debtor.amount,
                        creditor.amount
                    );

                    const id = Date.now() + Math.random();

                    if (!completedSettlementIds.includes(id)) {
                        settlements.push({
                            id,
                            from: debtor.name,
                            to: creditor.name,
                            amount: payAmount,
                        });
                    }

                    debtor.amount -= payAmount;
                    creditor.amount -= payAmount;
                }
            });
        });

        return settlements;
    };

    const settlements = generateSettlements();

    const markSettlementPaid = (settlement: Settlement) => {
        setCompletedSettlementIds([
            ...completedSettlementIds,
            settlement.id,
        ]);

        setSettlementHistory([
            ...settlementHistory,
            {
                ...settlement,
                completedAt: new Date().toLocaleString(),
            },
        ]);
    };

    return (
        <div className="bg-white/90 backdrop-blur-lg rounded-3xl shadow-xl border border-gray-100 p-8">

            {/* Heading */}
            <h2 className="text-4xl font-bold mb-8 bg-gradient-to-r from-purple-600 to-pink-500 bg-clip-text text-transparent">
                Expense Manager
            </h2>

            {/* Budget Cards */}
            <div className="grid md:grid-cols-3 gap-6 mb-10">
                <div className="bg-gradient-to-r from-purple-600 to-purple-800 text-white p-6 rounded-3xl shadow-lg">
                    <p>Total Budget</p>
                    <h3 className="text-3xl font-bold mt-2">₹{totalBudget}</h3>
                </div>

                <div className="bg-gradient-to-r from-red-500 to-pink-500 text-white p-6 rounded-3xl shadow-lg">
                    <p>Total Spent</p>
                    <h3 className="text-3xl font-bold mt-2">₹{totalSpent}</h3>
                </div>

                <div className="bg-gradient-to-r from-green-500 to-green-700 text-white p-6 rounded-3xl shadow-lg">
                    <p>Remaining</p>
                    <h3 className="text-3xl font-bold mt-2">₹{remaining}</h3>
                </div>
            </div>

            {/* Group Setup */}
            <div className="bg-gradient-to-br from-gray-50 to-purple-50 p-6 rounded-3xl mb-8">
                <h3 className="text-2xl font-bold mb-5">Group Setup</h3>

                <input
                    type="number"
                    placeholder="Total Number of People"
                    className={`${inputStyle} mb-4`}
                    onChange={(e) =>
                        handlePeopleCount(Number(e.target.value))
                    }
                />

                {people.map((person, index) => (
                    <div
                        key={index}
                        className="bg-white p-5 rounded-2xl shadow-sm mb-4"
                    >
                        <input
                            type="text"
                            placeholder="Enter Name"
                            value={person.name}
                            onChange={(e) =>
                                handlePersonName(index, e.target.value)
                            }
                            className={`${inputStyle} mb-3`}
                        />

                        <input
                            type="file"
                            onChange={(e: any) =>
                                handleQRUpload(index, e.target.files[0])
                            }
                        />
                    </div>
                ))}
            </div>

            {/* Add Expense */}
            <div className="bg-gradient-to-br from-white to-purple-50 p-6 rounded-3xl border border-purple-100 mb-8">
                <h3 className="text-2xl font-bold mb-5">Add Expense</h3>

                <div className="grid md:grid-cols-2 gap-4">
                    <input
                        placeholder="Expense Name"
                        value={expenseName}
                        onChange={(e) =>
                            setExpenseName(e.target.value)
                        }
                        className={inputStyle}
                    />

                    <input
                        placeholder="Amount"
                        value={amount}
                        onChange={(e) =>
                            setAmount(e.target.value)
                        }
                        className={inputStyle}
                    />

                    <select
                        value={paidBy}
                        onChange={(e) =>
                            setPaidBy(e.target.value)
                        }
                        className={inputStyle}
                    >
                        <option>Select User</option>
                        {people.map((person, index) => (
                            <option key={index} value={person.name}>
                                {person.name}
                            </option>
                        ))}
                    </select>

                    <select
                        value={category}
                        onChange={(e) =>
                            setCategory(e.target.value)
                        }
                        className={inputStyle}
                    >
                        <option>Food</option>
                        <option>Hotel</option>
                        <option>Transport</option>
                        <option>Shopping</option>
                        <option>Activities</option>
                    </select>
                </div>

                <textarea
                    placeholder="Expense Note"
                    value={note}
                    onChange={(e) =>
                        setNote(e.target.value)
                    }
                    className={`${inputStyle} mt-4`}
                />

                <button
                    onClick={addExpense}
                    className="w-full mt-5 bg-gradient-to-r from-purple-600 to-pink-500 text-white py-4 rounded-2xl font-semibold hover:scale-[1.02] transition"
                >
                    Add Expense
                </button>
            </div>

            {/* Pending Payments */}
            <div className="mb-8">
                <h3 className="text-2xl font-bold mb-4">
                    Pending Payments
                </h3>

                {expenses.map((expense) => (
                    <div
                        key={expense.id}
                        className="bg-white border-l-4 border-yellow-400 p-5 rounded-2xl shadow-sm mb-4 flex justify-between items-center"
                    >
                        <div>
                            <p className="font-bold text-lg">
                                {expense.paidBy} paid ₹{expense.amount}
                            </p>
                            <p className="text-gray-500">
                                For {expense.name}
                            </p>
                        </div>

                        <button
                            onClick={() =>
                                markExpensePaid(expense.id)
                            }
                            className="bg-gradient-to-r from-green-500 to-green-700 text-white px-5 py-2 rounded-xl"
                        >
                            Confirm
                        </button>
                    </div>
                ))}
            </div>

            {/* Split Result */}
            <div className="bg-gradient-to-br from-green-50 to-emerald-100 p-6 rounded-3xl mb-8">
                <h3 className="text-2xl font-bold mb-4">
                    Split Result
                </h3>

                {settlements.length > 0 ? (
                    settlements.map((settlement, index) => (
                        <div
                            key={index}
                            className="bg-white p-5 rounded-2xl shadow-sm border border-green-100 mb-4 flex justify-between items-center"
                        >
                            <div>
                                <p className="font-bold text-lg">
                                    {settlement.from} needs to pay {settlement.to}
                                </p>
                                <p className="text-red-600 font-semibold">
                                    ₹{settlement.amount.toFixed(0)}
                                </p>
                            </div>

                            <label className="flex items-center gap-2 bg-green-100 px-4 py-2 rounded-xl cursor-pointer">
                                <input
                                    type="checkbox"
                                    onChange={() =>
                                        markSettlementPaid(settlement)
                                    }
                                />
                                Payment Done
                            </label>
                        </div>
                    ))
                ) : (
                    <p>No pending split</p>
                )}
            </div>

            {/* Category Analytics */}
            <div className="bg-gradient-to-br from-blue-50 to-indigo-100 p-6 rounded-3xl mb-8">
                <h3 className="text-2xl font-bold mb-4">
                    Category Analytics
                </h3>

                {Object.keys(categoryTotals).map((cat) => (
                    <div
                        key={cat}
                        className="bg-white p-4 rounded-2xl shadow-sm flex justify-between mb-3"
                    >
                        <span className="font-medium">{cat}</span>
                        <span className="font-bold text-purple-600">
                            ₹{categoryTotals[cat]}
                        </span>
                    </div>
                ))}
            </div>

            {/* Payment History */}
            <div>
                <h3 className="text-2xl font-bold mb-4">
                    Payment History
                </h3>

                {completedExpenses.map((expense) => (
                    <div
                        key={expense.id}
                        className={`${cardStyle} p-5 mb-4`}
                    >
                        <p className="font-bold text-lg">
                            {expense.paidBy} paid ₹{expense.amount}
                        </p>
                        <p className="text-gray-500">
                            For {expense.name}
                        </p>
                        <p className="text-green-600 text-sm mt-2">
                            {expense.createdAt}
                        </p>
                    </div>
                ))}

                {settlementHistory.map((settlement, index) => (
                    <div
                        key={index}
                        className="bg-gradient-to-r from-blue-50 to-purple-50 p-5 rounded-2xl shadow-sm mb-4"
                    >
                        <p className="font-bold text-lg">
                            {settlement.from} paid ₹
                            {settlement.amount.toFixed(0)} to{" "}
                            {settlement.to}
                        </p>

                        <p className="text-green-600 text-sm mt-2">
                            {settlement.completedAt}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}