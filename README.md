# Steam Games Picker

**Navigate Your Vast Game Library with Ease!**

The Steam Games Picker is a powerful backend system designed to help you (and your friends!) effortlessly narrow down a massive collection of games to find that perfect next pick. Tired of endless scrolling and indecision? This application intelligently filters, sorts, and presents games in manageable batches, keeping track of your journey every step of the way.

## Features:

*   **Intelligent Batch Generation**: Dynamically creates batches of games, reducing the number of choices as you progress.
*   **Interactive Filtering**:
    *   **Finds common games** shared with selected friends.
    *   **Hard filters** by multiple tags, ensuring games possess *all* specified genres or characteristics.
    *   **Filters by playtime**, helping you discover quick sessions or epic sagas.
*   **Comprehensive Tag Extraction**: Automatically gathers all unique tags from your game library for easy filtering options.
*   **Robust State Management (Undo/Redo)**: Never fear a wrong decision! The app maintains a full history of your filtering process, allowing you to freely undo and redo steps until you find your ideal game.
*   **Final Pick Identification**: Clearly identifies the single chosen game once the selection process is complete.
*   **Modular & Tested Design**: Built with robust validation and unit-tested components, ensuring reliability and maintainability.

## How It Works (Core Logic):

The system leverages a sophisticated `Session` manager that orchestrates `State` objects, each representing a unique snapshot of your game selection journey. Games are intelligently moved between `"remaining,"` `"batch,"` and `"seen"` pools, driven by your confirmations and filtering choices. Core utilities handle complex operations like set intersections for common games and and precise tag-based filtering.
