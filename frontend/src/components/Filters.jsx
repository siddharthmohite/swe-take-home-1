import { useState } from 'react';

function Filters({ locations, metrics, filters, onFilterChange, onApplyFilters }) {
  const [localFilters, setLocalFilters] = useState(filters);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setLocalFilters(prev => ({ ...prev, [name]: value }));
    onFilterChange({ ...localFilters, [name]: value });
  };

  const handleApply = () => {
    onApplyFilters();
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold text-eco-primary mb-4">Filter Data</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <select
          name="locationId"
          value={localFilters.locationId}
          onChange={handleChange}
          className="p-2 border rounded"
        >
          <option value="">All Locations</option>
          {locations.map(loc => (
            <option key={loc.id} value={loc.id}>{loc.name}</option>
          ))}
        </select>
        <select
          name="metric"
          value={localFilters.metric}
          onChange={handleChange}
          className="p-2 border rounded"
        >
          <option value="">All Metrics</option>
          {metrics.map(met => (
            <option key={met.id} value={met.name}>{met.name}</option>
          ))}
        </select>
        <input
          type="date"
          name="startDate"
          value={localFilters.startDate}
          onChange={handleChange}
          className="p-2 border rounded"
        />
        <input
          type="date"
          name="endDate"
          value={localFilters.endDate}
          onChange={handleChange}
          className="p-2 border rounded"
        />
        <select
          name="qualityThreshold"
          value={localFilters.qualityThreshold}
          onChange={handleChange}
          className="p-2 border rounded"
        >
          <option value="">All Qualities</option>
          {['poor', 'questionable', 'good', 'excellent'].map(q => (
            <option key={q} value={q}>{q}</option>
          ))}
        </select>
        <select
          name="analysisType"
          value={localFilters.analysisType}
          onChange={handleChange}
          className="p-2 border rounded"
        >
          <option value="raw">Raw Data</option>
          <option value="trends">Trends</option>
          <option value="weighted">Summary</option>
        </select>
        <button
          onClick={handleApply}
          className="bg-eco-primary text-white p-2 rounded hover:bg-eco-dark transition"
        >
          Apply Filters
        </button>
      </div>
    </div>
  );
}

export default Filters;