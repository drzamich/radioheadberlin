// ==UserScript==
// @name         Auto Click Innenraum or Reihe
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Waits for "Innenraum" text to appear and clicks it, falls back to "Reihe" if not found
// @match        *://*/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    const PRIMARY_TEXT = 'Innenraum';
    const FALLBACK_TEXT = 'Reihe';
    const CHECK_INTERVAL = 200; // Check every 200ms

    let clicked = false;

    // Function to find and click Card element containing text
    function findAndClick(text) {
        const cards = document.querySelectorAll('div.EventEntryRow');
        
        for (let card of cards) {
            const textContent = card.textContent || '';
            
            if (textContent.includes(text)) {
                console.log(`Found and clicking Row with text: "${text}"`);
                card.click();
                return true;
            }
        }
        return false;
    }

    // Start checking for texts
    function startScript() {
        const checkInterval = setInterval(() => {
            if (clicked) {
                clearInterval(checkInterval);
                return;
            }

            // Try primary text first
            if (findAndClick(PRIMARY_TEXT)) {
                console.log(`Successfully clicked "${PRIMARY_TEXT}"`);
                clicked = true;
                clearInterval(checkInterval);
                return;
            }

            // If primary not found, immediately try fallback
            if (findAndClick(FALLBACK_TEXT)) {
                console.log(`Successfully clicked fallback "${FALLBACK_TEXT}"`);
                clicked = true;
                clearInterval(checkInterval);
                return;
            }
        }, CHECK_INTERVAL);
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', startScript);
    } else {
        startScript();
    }
})();