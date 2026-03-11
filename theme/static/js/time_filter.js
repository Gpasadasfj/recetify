const range = document.getElementById("timeRange");
const output = document.getElementById("timeValue");

const labels = ["Todos", "< 5 min", "< 15 min", "< 30 min", "< 1 h", "< 2 h"];

range.addEventListener("input", () => {
  output.textContent = labels[range.value];
});
