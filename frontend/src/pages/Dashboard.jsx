import { useEffect, useState } from "react";
import api from "../services/api";

const cleanText = (text) => {
  return text?.replace(/\*\*/g, "") || "";
};

function Dashboard() {
  const [rawUpdate, setRawUpdate] = useState("");
  const [summaries, setSummaries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [analytics, setAnalytics] = useState(null);
  const token = localStorage.getItem("token");

  const fetchSummaries = async () => {
    try {
      const response = await api.get("/summaries", {
        headers: { Authorization: `Bearer ${token}` },
      });

      setSummaries(response.data);
    } catch (error) {
      console.error(error);
    }

    const analyticsResponse = await api.get("/analytics", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    
    setAnalytics(analyticsResponse.data);
};

  useEffect(() => {
    fetchSummaries();
  }, []);

  const generateSummary = async () => {
    if (!rawUpdate.trim()) {
      setSuccessMessage("Please enter a project update first.");
      return;
    }

    try {
      setLoading(true);
      setSuccessMessage("");

      await api.post(
        "/generate-summary",
        { raw_update: rawUpdate },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setRawUpdate("");
      setSuccessMessage("Summary generated successfully ✅");
      fetchSummaries();
    } catch (error) {
      console.error(error);
      setSuccessMessage("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const deleteSummary = async (id) => {
    try {
      await api.delete(`/summaries/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      fetchSummaries();
    } catch (error) {
      console.error(error);
    }
  };

  const copyEmailDraft = async (emailDraft) => {
    try {
      await navigator.clipboard.writeText(cleanText(emailDraft));
      setSuccessMessage("Email draft copied to clipboard ✅");
    } catch (error) {
      console.error(error);
      setSuccessMessage("Could not copy email draft.");
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    window.location.reload();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-6 py-10">
      <div className="max-w-5xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold">
              AI Client Communication Hub
            </h1>
            {analytics && (
  <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
    
    <div className="bg-slate-800 p-5 rounded-xl border border-slate-700">
      <p className="text-slate-400 text-sm">
        Total Users
      </p>
      <h3 className="text-3xl font-bold text-white mt-2">
        {analytics.total_users}
      </h3>
    </div>

    <div className="bg-slate-800 p-5 rounded-xl border border-slate-700">
      <p className="text-slate-400 text-sm">
        Total Summaries
      </p>
      <h3 className="text-3xl font-bold text-white mt-2">
        {analytics.total_summaries}
      </h3>
    </div>

    <div className="bg-slate-800 p-5 rounded-xl border border-slate-700">
      <p className="text-slate-400 text-sm">
        My Summaries
      </p>
      <h3 className="text-3xl font-bold text-white mt-2">
        {analytics.my_summaries}
      </h3>
    </div>

    <div className="bg-slate-800 p-5 rounded-xl border border-slate-700">
      <p className="text-slate-400 text-sm">
        Logged In User
      </p>
      <h3 className="text-lg font-semibold text-green-400 mt-2">
        {analytics.current_user}
      </h3>
    </div>

  </div>
)}
            <p className="text-slate-400 mt-2">
              Generate client-ready summaries from technical project updates.
            </p>
          </div>

          <button
            onClick={logout}
            className="bg-slate-700 px-4 py-2 rounded-lg hover:bg-slate-600"
          >
            Logout
          </button>
        </div>

        {successMessage && (
          <div className="mb-6 rounded-lg bg-slate-800 border border-slate-700 p-4 text-green-400">
            {successMessage}
          </div>
        )}

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-10 shadow-xl">
          <label className="block text-lg font-semibold mb-3">
            Project Update
          </label>

          <textarea
            className="w-full h-40 p-4 rounded-xl bg-slate-800 text-white border border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
            placeholder="Example: Completed onboarding API integration, fixed authentication issues, and started deployment validation..."
            value={rawUpdate}
            onChange={(e) => setRawUpdate(e.target.value)}
          />

          <button
            onClick={generateSummary}
            disabled={loading}
            className="bg-blue-600 px-6 py-3 rounded-xl hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
                Generating...
              </span>
            ) : (
              "Generate Summary"
            )}
          </button>
        </div>

        <div className="mb-6">
          <h2 className="text-2xl font-bold">Generated Summaries</h2>
          <p className="text-slate-400 mt-1">
            Review previously generated client communication drafts.
          </p>
        </div>

        {summaries.length === 0 && (
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-8 text-center text-slate-400">
            No summaries generated yet.
          </div>
        )}

        {summaries.map((summary) => (
          <div
            key={summary.id}
            className="bg-slate-800 rounded-2xl p-8 mb-8 shadow-xl text-left border border-slate-700"
          >
            <p className="text-sm text-slate-400 mb-4">ID: {summary.id}</p>

            <h3 className="text-lg font-semibold text-blue-300">Summary</h3>
            <p className="text-slate-200 mb-5">
              {cleanText(summary.summary)}
            </p>

            <h3 className="text-lg font-semibold text-yellow-300">Risks</h3>
            <p className="text-slate-200 mb-5">
              {cleanText(summary.risks)}
            </p>

            <h3 className="text-lg font-semibold text-green-300">
              Next Steps
            </h3>
            <p className="text-slate-200 mb-5">
              {cleanText(summary.next_steps)}
            </p>

            <details className="mt-4">
              <summary className="cursor-pointer text-purple-300 font-semibold">
                View Email Draft
              </summary>

              <div className="mt-4 whitespace-pre-line text-slate-200 bg-slate-900 border border-slate-700 rounded-xl p-4">
                {cleanText(summary.email_draft)}
              </div>
            </details>

            <div className="flex gap-3 mt-6">
              <button
                onClick={() => copyEmailDraft(summary.email_draft)}
                className="bg-slate-700 px-4 py-2 rounded-lg hover:bg-slate-600"
              >
                Copy Email
              </button>

              <button
                onClick={() => deleteSummary(summary.id)}
                className="bg-red-600 px-4 py-2 rounded-lg hover:bg-red-700"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;