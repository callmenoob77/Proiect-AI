import React from "react";
import { GitBranch } from "lucide-react";

export default function TreeVisualizer({ tree }) {
  if (!tree) return null;

  // Calculează layout-ul (width pentru fiecare subarbore)
  const computeWidth = (node) => {
    if ("value" in node) {
      node._width = 1;
      return 1;
    }
    let total = 0;
    for (let child of node.children) {
      total += computeWidth(child);
    }
    node._width = total;
    return total;
  };

  computeWidth(tree);

  // Render recursiv cu spațiere proporțională
  const renderNode = (node) => {
    const isLeaf = "value" in node;
    const nodeType = node.type || "LEAF";

    const colors = {
      MAX: "bg-blue-500 text-white border-blue-600",
      MIN: "bg-red-500 text-white border-red-600",
      LEAF: "bg-green-500 text-white border-green-600",
    };

    return (
      <div
        style={{ minWidth: `${node._width * 80}px` }}
        className="flex flex-col items-center"
      >
        {/* NOD */}
        <div
          className={`${colors[nodeType]} border-2 rounded-lg px-4 py-2 font-bold text-sm shadow-lg`}
        >
          {isLeaf ? node.value : nodeType}
        </div>

        {/* Dacă nu e frunză → desenează copiii */}
        {!isLeaf && node.children?.length > 0 && (
          <>
            {/* Bara verticală sub nod */}
            <div className="h-6 w-0.5 bg-gray-400"></div>

            {/* 🔥 Bara orizontală care unește copiii */}
            <div
              className="bg-gray-400"
              style={{
                height: "2px",
                width: `${node._width * 80}px`,
                marginBottom: "4px",
              }}
            ></div>

            {/* Grup copii */}
            <div className="flex">
              {node.children.map((child, i) => (
                <div
                  key={child.id || i}
                  className="flex flex-col items-center"
                  style={{ minWidth: `${child._width * 80}px` }}
                >
                  {/* Bara verticală pentru fiecare copil */}
                  <div className="h-6 w-0.5 bg-gray-400"></div>
                  {renderNode(child)}
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    );
  };

  return (
    <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-8 mb-6 border-2 border-gray-200 overflow-x-auto">
      <div className="flex items-center gap-2 mb-4">
        <GitBranch className="w-5 h-5 text-gray-600" />
        <h3 className="text-lg font-semibold text-gray-800">Arbore de joc</h3>
      </div>

      {/* Legendă */}
      <div className="flex gap-4 mb-6 text-sm">
        <Legend color="bg-blue-500 border-blue-600" text="MAX" />
        <Legend color="bg-red-500 border-red-600" text="MIN" />
        <Legend color="bg-green-500 border-green-600" text="Frunză (valoare)" />
      </div>

      <div className="flex justify-center py-4">
        {renderNode(tree)}
      </div>
    </div>
  );
}

function Legend({ color, text }) {
  return (
    <div className="flex items-center gap-2">
      <div className={`w-4 h-4 ${color} rounded border-2`} />
      <span className="text-gray-700">{text}</span>
    </div>
  );
}
