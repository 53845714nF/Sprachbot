import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';
import { User } from '../types/user';

interface UserCountChartProps {
  users: User[];
}

const UserCountChart: React.FC<UserCountChartProps> = ({ users }) => {
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (users && users.length > 0 && chartRef.current) {
      // Clear previous chart
      d3.select(chartRef.current).select('svg').remove();

      // Aggregate data
      const cityCounts = d3.rollup(
        users,
        (v) => v.length,
        (d) => d.adresse.ort
      );
      const sortedCityCounts = Array.from(cityCounts).sort(([, a], [, b]) => b - a);
      const data = sortedCityCounts.map(([city, count]) => ({ city, count }));

      const margin = { top: 20, right: 30, bottom: 70, left: 60 };
      const width = 600 - margin.left - margin.right;
      const height = 350 - margin.top - margin.bottom;

      // Create SVG
      const svg = d3.select(chartRef.current)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .attr('class', 'bg-white rounded-xl shadow-md')
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      // X axis
      const x = d3.scaleBand()
        .domain(data.map(d => d.city))
        .range([0, width])
        .padding(0.1);
      svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .selectAll('text')
        .attr('transform', 'rotate(-45)')
        .style('text-anchor', 'end')
        .style('font-size', '0.75rem')
        .style('fill', '#4B5563'); // Tailwind text-gray-700

      // Y axis
      const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.count) as number])
        .nice()
        .range([height, 0]);
      svg.append('g')
        .call(d3.axisLeft(y))
        .selectAll('text')
        .style('font-size', '0.75rem')
        .style('fill', '#4B5563');

      // Bars
      svg.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('x', d => x(d.city)!)
        .attr('y', d => y(d.count))
        .attr('width', x.bandwidth())
        .attr('height', d => height - y(d.count))
        .attr('fill', '#3B82F6'); // Tailwind blue-500
    }
  }, [users]);

  return (
    <div className="overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-800">Nutzer pro Stadt</h2>
        <p className="mt-1 text-sm text-gray-600">Zeigt die Anzahl der Nutzer pro Stadt an</p>
      </div>
      <div className="p-6">
        <div ref={chartRef} className="overflow-x-auto" />
      </div>
    </div>
  );
};

export default UserCountChart;
