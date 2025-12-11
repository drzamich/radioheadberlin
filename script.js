// ==UserScript==
// @name         Auto Click Innenraum or Reihe
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Waits for "Innenraum" text to appear and clicks it, falls back to "Reihe" if not found
// @match        https://www.fansale.de/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function () {
  "use strict";

  // Check if script is already running
  if (window.__radioheadScriptRunning) {
    console.log("[RADIOBOT] ", "Script is already running, exiting");
    return;
  }
  window.__radioheadScriptRunning = true;

  const PRIMARY_TEXT = "Innenraum";
  const FALLBACK_TEXT = "Unterrang";
  const CHECKOUT_TEXT = "ZUR KASSE";
  const ACCESS_DENIED_TEXT = "Access Denied";
  const CHECK_INTERVAL = 50; // Check every 200ms
  const CHECKOUT_TIMEOUT = 4000; // Wait 2 seconds for checkout button
  const RELOAD_TIMEOUT = 12 * 1000; // Wait 12 seconds for initial text
  const SUCCESS_AUDIO_URL = "https://www.myinstants.com/media/sounds/mlg-airhorn.mp3";
  const SUCCESS_URL = "https://www.youtube.com/watch?v=jNY_wLukVW0?autoplay=1";
  const ACCESS_DENIED_URL =
    "https://www.youtube.com/watch?v=w7nrYizajmk?autoplay=1";

  let clicked = false;
  let checkoutClicked = false;

  function openUrlInNewTab(url) {
    console.log("[RADIOBOT] open url in new tab", url);
    window.open(url, "_blank");
  }

  // Play success notification
  function playSuccessNotification() {
    console.log("[RADIOBOT] ", "Playing success audio");
    const audio = new Audio(SUCCESS_AUDIO_URL);
    audio.volume = 1.0;
    audio.play().catch(err => console.log("[RADIOBOT] ", "Audio play failed:", err));
  }

  // Function to find and click Card element containing text
  function findAndClick(text) {
    const cards = document.querySelectorAll(".OfferEntry-SeatDescription");

    for (let card of cards) {
      const textContent = card.textContent || "";

      if (textContent.includes(text)) {
        console.log(
          "[RADIOBOT] ",
          `Found and clicking Row with text: "${text}"`
        );
        card.click();
        return true;
      }
    }
    console.log("[RADIOBOT] ", text, "not found");
    return false;
  }

  // Function to find and click checkout button
  function findAndClickCheckout() {
    const allElements = document.querySelectorAll(".DetailCSection button");

    for (let element of allElements) {
      const textContent = element.textContent || "";

      if (textContent.includes(CHECKOUT_TEXT)) {
        console.log(
          "[RADIOBOT] ",
          `Found and clicking checkout button: "${CHECKOUT_TEXT}"`
        );
        console.log("[RADIOBOT] ", element);
        element.click();
        return true;
      }
    }
    return false;
  }

  // Start checking for checkout button
  function startCheckoutCheck() {
    console.log("[RADIOBOT] ", "Looking for", CHECKOUT_TEXT);
    const startTime = Date.now();

    const checkoutInterval = setInterval(() => {
      if (checkoutClicked) {
        clearInterval(checkoutInterval);
        return;
      }

      if (findAndClickCheckout()) {
        console.log("[RADIOBOT] ", `Successfully clicked "${CHECKOUT_TEXT}"`);
        checkoutClicked = true;
        clearInterval(checkoutInterval);

        playSuccessNotification();

        // Stop the script
        window.__radioheadScriptRunning = false;
        return;
      }

      // If timeout exceeded, go back in history
      if (Date.now() - startTime > CHECKOUT_TIMEOUT) {
        console.log(
          "[RADIOBOT] ",
          `"${CHECKOUT_TEXT}" not found after ${CHECKOUT_TIMEOUT}ms, going back in history`
        );
        clearInterval(checkoutInterval);
        window.history.back();

        console.log("[RADIOBOT] ", "Reloading page...");
        // Wait 7 seconds and reload the page
        setTimeout(() => {
          window.location.reload();
        }, RELOAD_TIMEOUT - 4000);
      }
    }, CHECK_INTERVAL);
  }

  // Check for Access Denied
  function checkAccessDenied() {
    const h1Elements = document.querySelectorAll("h1");
    for (let h1 of h1Elements) {
      if (h1.textContent.includes(ACCESS_DENIED_TEXT)) {
        console.log(
          "[RADIOBOT] ",
          `Found "${ACCESS_DENIED_TEXT}", redirecting to ${ACCESS_DENIED_URL}`
        );
        openUrlInNewTab(ACCESS_DENIED_URL, "_blank");
        return true;
      }
    }
    return false;
  }

  // Start checking for texts
  function startScript() {
    // Check for Access Denied first
    if (checkAccessDenied()) {
      return;
    }

    const startTime = Date.now();

    const checkInterval = setInterval(() => {
      if (clicked) {
        clearInterval(checkInterval);
        return;
      }

      // Check for Access Denied on each iteration
      if (checkAccessDenied()) {
        clearInterval(checkInterval);
        return;
      }

      // Try primary text first
      if (findAndClick(PRIMARY_TEXT)) {
        console.log("[RADIOBOT] ", `Successfully clicked "${PRIMARY_TEXT}"`);
        clicked = true;
        clearInterval(checkInterval);
        startCheckoutCheck();
        return;
      }

      // If primary not found, immediately try fallback
      if (findAndClick(FALLBACK_TEXT)) {
        console.log(
          "[RADIOBOT] ",
          `Successfully clicked fallback "${FALLBACK_TEXT}"`
        );
        clicked = true;
        clearInterval(checkInterval);
        startCheckoutCheck();
        return;
      }

      // If timeout exceeded, reload the page
      if (Date.now() - startTime > RELOAD_TIMEOUT) {
        console.log(
          "[RADIOBOT] ",
          `No text found after ${RELOAD_TIMEOUT}ms, reloading page`
        );
        clearInterval(checkInterval);
        window.location.reload();
      }
    }, CHECK_INTERVAL);
  }

  // Wait for DOM to be ready
  if (document.readyState === "loading") {
    console.log("[RADIOBOT] ", "starting srcript");
    document.addEventListener("DOMContentLoaded", startScript);
  } else {
    startScript();
  }
})();
