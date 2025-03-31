function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}
document.addEventListener('DOMContentLoaded', () => {
  // Add event listener for star rating click
  document.querySelectorAll('.star-rating i').forEach(star => {
      star.addEventListener('click', (e) => {
          const value = e.target.getAttribute('data-value');
          const requestId = e.target.getAttribute('data-id');
          const ratingInput = document.getElementById(`rating-input-${requestId}`);
          const stars = document.querySelectorAll(`#rating-${requestId} i`);

          // Set the hidden input value
          ratingInput.value = value;

          // Highlight the selected stars
          stars.forEach((s, index) => {
              if (index < value) {
                  s.classList.remove('far');
                  s.classList.add('fas');
              } else {
                  s.classList.remove('fas');
                  s.classList.add('far');
              }
          });
      });
  });

  // Initialize stars for "View Review" modals based on existing ratings
  document.querySelectorAll('.modal').forEach(modal => {
      const requestId = modal.id.replace('viewreview', ''); // Extract request ID
      const ratingInput = document.getElementById(`rating-input-${requestId}`);
      if (ratingInput) {
          const rating = parseInt(ratingInput.value, 10) || 0; // Get the rating value
          const stars = document.querySelectorAll(`#rating-${requestId} i`);

          // Highlight stars according to the saved rating
          stars.forEach((star, index) => {
              if (index < rating) {
                  star.classList.remove('far');
                  star.classList.add('fas'); // Filled star
              } else {
                  star.classList.remove('fas');
                  star.classList.add('far'); // Empty star
              }
          });
      }
  });
});
