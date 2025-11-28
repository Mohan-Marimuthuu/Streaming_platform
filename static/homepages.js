 function setupCarousel(carouselElem) {
            const track = carouselElem.querySelector('[data-carousel-track]');
            const prevButton = carouselElem.querySelector('[data-carousel-button="prev"]');
            const nextButton = carouselElem.querySelector('[data-carousel-button="next"]');
            let currentOffset = 0;

            function updateButtons() {
                // Check if we are at the beginning
                prevButton.classList.toggle('hidden', currentOffset === 0);

                // Check if we are at the end
                // scrollWidth is the total width of all items
                // clientWidth is the visible width of the container
                const isAtEnd = currentOffset <= -(track.scrollWidth - track.clientWidth - 1);
                nextButton.classList.toggle('hidden', isAtEnd);
            }

            nextButton.addEventListener('click', () => {
                const cardWidth = track.querySelector('.show-card').offsetWidth;
                const gap = parseInt(window.getComputedStyle(track).gap);
                const scrollAmount = cardWidth + gap;

                // Move left by scrollAmount, but don't go past the end
                const maxOffset = -(track.scrollWidth - track.clientWidth);
                currentOffset = Math.max(currentOffset - scrollAmount, maxOffset);
                
                track.style.transform = `translateX(${currentOffset}px)`;
                updateButtons();
            });

            prevButton.addEventListener('click', () => {
                const cardWidth = track.querySelector('.show-card').offsetWidth;
                const gap = parseInt(window.getComputedStyle(track).gap);
                const scrollAmount = cardWidth + gap;

                // Move right by scrollAmount, but not further than 0
                currentOffset = Math.min(currentOffset + scrollAmount, 0);

                track.style.transform = `translateX(${currentOffset}px)`;
                updateButtons();
            });

            // Initial button state check
            updateButtons();
            
            // Re-calculate on window resize
            window.addEventListener('resize', () => {
                // Reset to start on resize to avoid weird positioning
                currentOffset = 0;
                track.style.transform = `translateX(0px)`;
                updateButtons();
            });
        }
        
        // Initialize all carousels on the page
        document.querySelectorAll('[data-carousel]').forEach(setupCarousel);

