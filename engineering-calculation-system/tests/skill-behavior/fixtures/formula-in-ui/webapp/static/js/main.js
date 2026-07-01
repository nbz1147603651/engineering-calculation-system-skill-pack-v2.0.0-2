export function unsafeUiCalculation(input) {
  // Fixture only: production formulas must not live in UI JavaScript.
  const demand = input.load * input.factor;
  const capacity = input.width * input.depth * input.allowableStress;
  return { ratio: demand / capacity, status: demand <= capacity ? "pass" : "fail" };
}
