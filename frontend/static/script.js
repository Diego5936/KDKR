const tabContainers = document.querySelectorAll('.tab-content');
tabContainers.forEach(c => c.style.display = c.id === 'overview' ? 'block' : 'none');

const buttons = document.querySelectorAll('.rounded-btn');
const missionImage = document.getElementById('mission-image');

// Map each mission to its image file
const missionImages = {
  overview: "/static/mission_0.png",  // overview uses mission_0.png
  mission1: "/static/mission_0.png",  // mission1 also uses mission_0.png
  mission2: "/static/mission_1.png",
  mission3: "/static/mission_2.png",
  mission4: "/static/mission_3.png",
  mission5: "/static/mission_4.png",
  mission6: "/static/mission_5.png",
  mission7: "/static/mission_6.png",
  mission8: "/static/mission_7.png"   // last one (no mission_8.png)
};

// Initialize with overview image
if (missionImage) {
  missionImage.src = missionImages["overview"];
}

buttons.forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.getAttribute('data-tab');

    // Show correct left-column tab
    tabContainers.forEach(c => {
      c.style.display = c.id === tab ? 'block' : 'none';
    });

    // Update button active state
    buttons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    // Smoothly update right-side image
    if (missionImage && missionImages[tab]) {
      missionImage.classList.add('fade-out');
      setTimeout(() => {
        missionImage.src = missionImages[tab];
        missionImage.classList.remove('fade-out');
      }, 200);
    }
  });
});
