function reset(fieldId) {
  document.getElementById(fieldId).selectedIndex=0;
};

document.getElementById('resetBtnRegion').addEventListener('click', () => reset('region'));

document.getElementById('resetBtnSort').addEventListener('click', () => reset('sort_by'));

document.getElementById('resetBtnAll').addEventListener('click', function() {
  reset('region');
  reset('sort_by');
});
