import React from 'react';


// pt afisarea matricei cu care se adreseaza intrebarea
export default function GameMatrixVisualizer({ matrix }) {
    if (!matrix) return null;

    const { rows, cols, row_strategies, col_strategies, payoffs } = matrix;

    return (
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-6 mb-6">
            <h3 className="text-lg font-bold text-gray-800 mb-4 text-center">
                Matricea de Joc (Jucător 1, Jucător 2)
            </h3>

            <div className="overflow-x-auto">
                <table className="mx-auto border-collapse">
                    <thead>
                        <tr>
                            <th className="p-3 bg-gray-100 border-2 border-gray-300 rounded-tl-lg">
                                J1 \ J2
                            </th>
                            {col_strategies.map((strategy, idx) => (
                                <th
                                    key={idx}
                                    className="p-3 bg-blue-100 border-2 border-gray-300 font-semibold text-blue-800 min-w-[100px]"
                                >
                                    {strategy}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {payoffs.map((row, rowIdx) => (
                            <tr key={rowIdx}>
                                <td className="p-3 bg-purple-100 border-2 border-gray-300 font-semibold text-purple-800">
                                    {row_strategies[rowIdx]}
                                </td>
                                {row.map((cell, colIdx) => {
                                    const [p1, p2] = cell;
                                    return (
                                        <td
                                            key={colIdx}
                                            className="p-4 bg-white border-2 border-gray-300 text-center hover:bg-yellow-50 transition-colors"
                                        >
                                            <span className="text-purple-700 font-bold">{p1}</span>
                                            <span className="text-gray-400 mx-1">,</span>
                                            <span className="text-blue-700 font-bold">{p2}</span>
                                        </td>
                                    );
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="flex justify-center gap-6 mt-4 text-sm">
                <div className="flex items-center gap-2">
                    <span className="w-4 h-4 bg-purple-500 rounded"></span>
                    <span className="text-gray-600">Payoff Jucător 1 (alege rândul)</span>
                </div>
                <div className="flex items-center gap-2">
                    <span className="w-4 h-4 bg-blue-500 rounded"></span>
                    <span className="text-gray-600">Payoff Jucător 2 (alege coloana)</span>
                </div>
            </div>
        </div>
    );
}
