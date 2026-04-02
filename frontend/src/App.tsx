import { useMemo, useState } from "react";
import type { FormEvent } from "react";

type EducationLevel = "High School" | "Bachelor" | "Master" | "PhD";
type Gender = "Male" | "Female";

type PredictPayload = {
  age: number;
  years_of_experience: number;
  education_level: EducationLevel;
  gender: Gender;
  job_title: string;
};

type PredictResponse = {
  predicted_salary: number;
  input_data: PredictPayload;
};

export default function App() {
  const [age, setAge] = useState("30");
  const [yearsOfExperience, setYearsOfExperience] = useState("5");
  const [educationLevel, setEducationLevel] =
    useState<EducationLevel>("Bachelor");
  const [gender, setGender] = useState<Gender>("Male");
  const [jobTitle, setJobTitle] = useState("Software Engineer");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<PredictResponse | null>(null);

  const canSubmit = useMemo(() => {
    return (
      Number(age) >= 18 &&
      Number(age) <= 100 &&
      Number(yearsOfExperience) >= 0 &&
      Number(yearsOfExperience) <= 60 &&
      jobTitle.trim().length > 0
    );
  }, [age, yearsOfExperience, jobTitle]);

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setResult(null);

    const payload: PredictPayload = {
      age: Number(age),
      years_of_experience: Number(yearsOfExperience),
      education_level: educationLevel,
      gender,
      job_title: jobTitle.trim(),
    };

    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = (await response.json()) as
        | PredictResponse
        | { detail?: string };

      if (!response.ok) {
        const message =
          "detail" in data && data.detail ? data.detail : "Request failed";
        throw new Error(message);
      }

      setResult(data as PredictResponse);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative min-h-screen overflow-hidden bg-linear-to-br from-slate-100 via-white to-sky-100 px-4 py-10 sm:py-14">
      <div className="pointer-events-none absolute -left-20 -top-24 h-64 w-64 rounded-full bg-sky-200/50 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-24 -right-20 h-72 w-72 rounded-full bg-indigo-200/40 blur-3xl" />

      <div className="relative mx-auto w-full max-w-xl rounded-2xl border border-white/60 bg-white/90 p-6 shadow-[0_12px_40px_-18px_rgba(15,23,42,0.35)] backdrop-blur sm:p-7">
        <h1 className="text-2xl font-semibold tracking-tight text-slate-900 sm:text-3xl">
          Salary Predictor
        </h1>
        <p className="mt-2 text-sm text-slate-600">
          Enter details and get salary prediction.
        </p>

        <form
          onSubmit={handleSubmit}
          className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="sm:col-span-1">
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Age
            </label>
            <input
              type="number"
              min={18}
              max={100}
              value={age}
              onChange={(e) => setAge(e.target.value)}
              className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-800 outline-none transition duration-200 placeholder:text-slate-400 focus:border-sky-400 focus:ring-4 focus:ring-sky-100"
              required
            />
          </div>

          <div className="sm:col-span-1">
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Years of Experience
            </label>
            <input
              type="number"
              min={0}
              max={60}
              step="0.1"
              value={yearsOfExperience}
              onChange={(e) => setYearsOfExperience(e.target.value)}
              className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-800 outline-none transition duration-200 placeholder:text-slate-400 focus:border-sky-400 focus:ring-4 focus:ring-sky-100"
              required
            />
          </div>

          <div className="sm:col-span-1">
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Education Level
            </label>
            <select
              value={educationLevel}
              onChange={(e) =>
                setEducationLevel(e.target.value as EducationLevel)
              }
              className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-800 outline-none transition duration-200 focus:border-sky-400 focus:ring-4 focus:ring-sky-100">
              <option value="High School">High School</option>
              <option value="Bachelor">Bachelor</option>
              <option value="Master">Master</option>
              <option value="PhD">PhD</option>
            </select>
          </div>

          <div className="sm:col-span-1">
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Gender
            </label>
            <select
              value={gender}
              onChange={(e) => setGender(e.target.value as Gender)}
              className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-800 outline-none transition duration-200 focus:border-sky-400 focus:ring-4 focus:ring-sky-100">
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>

          <div className="sm:col-span-2">
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Job Title
            </label>
            <input
              type="text"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-800 outline-none transition duration-200 placeholder:text-slate-400 focus:border-sky-400 focus:ring-4 focus:ring-sky-100"
              required
            />
          </div>

          <button
            type="submit"
            disabled={!canSubmit || loading}
            className="sm:col-span-2 mt-1 w-full rounded-lg bg-linear-to-r from-slate-900 to-slate-700 px-4 py-2.5 text-sm font-medium text-white transition duration-200 hover:from-slate-800 hover:to-slate-700 disabled:cursor-not-allowed disabled:opacity-60">
            {loading ? "Predicting..." : "Predict Salary"}
          </button>
        </form>

        {error && (
          <p className="mt-5 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            {error}
          </p>
        )}

        {result && (
          <div className="mt-5 rounded-xl border border-emerald-200 bg-emerald-50/80 p-4 shadow-sm transition duration-300">
            <p className="text-sm font-medium text-emerald-800">
              Predicted Salary
            </p>
            <p className="mt-1 text-3xl font-semibold tracking-tight text-emerald-900">
              ${result.predicted_salary.toLocaleString()}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
