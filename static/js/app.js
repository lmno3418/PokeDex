document.addEventListener("DOMContentLoaded", function () {
  const searchBox = document.getElementById("search-box");
  const pokelist = document.getElementById("pokelist");
  const pokeResultCard = document.getElementById("poke-result-card");
  const filterToggle = document.getElementById("filter-toggle");
  const filterContainer = document.getElementById("filter-container");
  const filterChevron = document.getElementById("filter-chevron");
  const resetFiltersBtn = document.getElementById("reset-filters");
  const activeFiltersContainer = document.getElementById("active-filters");
  
  // Battle elements
  const battleBtn = document.getElementById("battle-btn");
  const battleResult = document.getElementById("battle-result");
  const battleWinner = document.getElementById("battle-winner");
  const battleConfidence = document.getElementById("battle-confidence");
  const pokemonSlot1 = document.getElementById("pokemon-slot-1");
  const pokemonSlot2 = document.getElementById("pokemon-slot-2");

  let allPokemons = [];
  let selectedPokemon = null;
  let currentFilters = {};
  let searchTerm = "";
  let sortOption = "id";
  
  // Battle state
  let battlePokemon1 = null;
  let battlePokemon2 = null;

  // Fetch all Pokemons on page load
  fetchPokemons();

  // Add event listener for search
  searchBox.addEventListener("input", function (event) {
    searchTerm = event.target.value.trim().toLowerCase();
    applyFiltersAndSearch();
  });

  // Toggle filter container
  filterToggle.addEventListener("click", function () {
    filterContainer.classList.toggle("active");
    filterChevron.classList.toggle("fa-chevron-down");
    filterChevron.classList.toggle("fa-chevron-up");
  });

  // Reset filters
  resetFiltersBtn.addEventListener("click", resetFilters);
  
  // Battle button event listener
  battleBtn.addEventListener("click", startBattle);

  function fetchPokemons() {
    showLoading();
    console.log("Fetching Pokemon data...");

    fetch("/api/pokemon")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log(`Successfully loaded ${data.length} Pokemon`);
        allPokemons = data;
        hideLoading();
        renderPokemonList(allPokemons);
      })
      .catch((error) => {
        console.error("Error fetching Pokemon data:", error);
        hideLoading();
        pokelist.innerHTML = `<h2 class="no-pokemon">Error loading Pokemon data: ${error.message}</h2>`;
      });
  }

  function showLoading() {
    pokelist.innerHTML = `
      <div class="loading">
        <div class="pokeball"></div>
      </div>
    `;
  }

  function hideLoading() {
    const loadingElement = document.querySelector(".loading");
    if (loadingElement) {
      loadingElement.remove();
    }
  }

  function sortPokemons(pokemons) {
    return [...pokemons].sort((a, b) => {
      switch (sortOption) {
        case "name":
          return a.name.localeCompare(b.name);
        case "hp":
          return b.hp - a.hp;
        case "attack":
          return b.attack - a.attack;
        case "defense":
          return b.defense - a.defense;
        case "speed":
          return b.speed - a.speed;
        default: // id
          return a.id - b.id;
      }
    });
  }

  function renderPokemonList(pokemons) {
    if (pokemons.length === 0) {
      pokelist.innerHTML = '<h2 class="no-pokemon">No pokemon found!</h2>';
      return;
    }

    // Validate the data format of the first Pokemon
    const firstPokemon = pokemons[0];
    if (!firstPokemon.name || !firstPokemon.id) {
      console.error("Invalid Pokemon data format:", firstPokemon);
      pokelist.innerHTML =
        '<h2 class="no-pokemon">Error: Invalid Pokemon data format!</h2>';
      return;
    }

    pokelist.innerHTML = "";

    // Sort pokemons
    const sortedPokemons = sortPokemons(pokemons);

    sortedPokemons.forEach((pokemon) => {
      if (!pokemon.name) return;

      const pokeCard = document.createElement("div");
      pokeCard.className = "pokecard";
      if (selectedPokemon && selectedPokemon.id === pokemon.id) {
        pokeCard.classList.add("selected");
      }
      pokeCard.addEventListener("click", () => handlePokemonClick(pokemon));

      // Parse the sprites JSON string if it's a string
      let sprites;
      if (typeof pokemon.sprites === "string") {
        try {
          sprites = JSON.parse(pokemon.sprites);
        } catch (e) {
          console.error("Error parsing sprites:", e);
          sprites = { normal: "", animated: "" };
        }
      } else {
        sprites = pokemon.sprites || { normal: "", animated: "" };
      }

      console.log("Pokemon:", pokemon.name, "Sprites:", sprites);

      const spriteUrl = sprites.normal || "";
      const legendaryBadge = pokemon.legendary
        ? '<span class="legendary-badge">★</span>'
        : "";

      // Add battle button to each Pokemon card
      const battleButtonHtml = `<button class="add-to-battle" data-id="${pokemon.id}">Add to Battle</button>`;

      pokeCard.innerHTML = `
                <div class="card-header">
                    <span class="pokemon-id">#${String(pokemon.id).padStart(
                      3,
                      "0"
                    )}</span>
                    ${legendaryBadge}
                </div>
                <img src="${spriteUrl}" alt="${pokemon.name}" class="pokemon">
                <h3 class="pokemon-name">${pokemon.name}</h3>
                <div class="card-types">
                    <span class="type-badge type-${pokemon.type1.toLowerCase()}">${
        pokemon.type1
      }</span>
                    ${
                      pokemon.type2
                        ? `<span class="type-badge type-${pokemon.type2.toLowerCase()}">${
                            pokemon.type2
                          }</span>`
                        : ""
                    }
                </div>
                <div class="card-stats">
                    <span title="HP"><i class="fas fa-heart"></i> ${
                      pokemon.hp
                    }</span>
                    <span title="Attack"><i class="fas fa-fist-raised"></i> ${
                      pokemon.attack
                    }</span>
                    <span title="Speed"><i class="fas fa-bolt"></i> ${
                      pokemon.speed
                    }</span>
                </div>
                ${battleButtonHtml}
            `;

      pokelist.appendChild(pokeCard);
    });
    
    // Add event listeners to battle buttons
    document.querySelectorAll('.add-to-battle').forEach(button => {
      button.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent triggering the card click event
        const pokemonId = parseInt(e.target.getAttribute('data-id'));
        const pokemon = allPokemons.find(p => p.id === pokemonId);
        if (pokemon) {
          addPokemonToBattle(pokemon);
        }
      });
    });
  }

  function handlePokemonClick(pokemon) {
    selectedPokemon = pokemon;
    renderPokemonDetails();

    // Update selected state in the list
    document.querySelectorAll(".pokecard").forEach((card) => {
      card.classList.remove("selected");
    });

    // Find and select the current card
    const cards = document.querySelectorAll(".pokecard");
    for (let i = 0; i < cards.length; i++) {
      if (
        cards[i].querySelector(".pokemon-name").textContent === pokemon.name
      ) {
        cards[i].classList.add("selected");
        break;
      }
    }
  }

  function renderPokemonDetails() {
    if (!selectedPokemon) {
      pokeResultCard.innerHTML = `
                <h2>Welcome to the Pokedex</h2>
                <p class="info-text">Select a Pokémon to view details</p>
            `;
      return;
    }

    // Parse the sprites JSON string if it's a string
    let sprites;
    if (typeof selectedPokemon.sprites === "string") {
      try {
        sprites = JSON.parse(selectedPokemon.sprites);
      } catch (e) {
        console.error("Error parsing sprites in details view:", e);
        sprites = { normal: "", animated: "" };
      }
    } else {
      sprites = selectedPokemon.sprites || { normal: "", animated: "" };
    }

    console.log("Selected Pokemon:", selectedPokemon.name, "Sprites:", sprites);

    const spriteUrl = sprites.animated || sprites.normal || "";
    const type2Display = selectedPokemon.type2 ? selectedPokemon.type2 : "None";
    const legendaryStatus = selectedPokemon.legendary ? "Yes" : "No";
    
    // Add battle button to details view
    const battleButtonHtml = `<button class="add-to-battle" id="detail-battle-btn" data-id="${selectedPokemon.id}">Add to Battle</button>`;

    pokeResultCard.innerHTML = `
            <img src="${spriteUrl}" alt="${selectedPokemon.name}" class="pokemon-animated-sprite">
            <div class="pokemon-details">
                <h3>#${String(selectedPokemon.id).padStart(3, "0")} - ${selectedPokemon.name}</h3>
                ${battleButtonHtml}
                
                <div class="stat-grid">
                    <div class="stat-group">
                        <h4>Pokémon Info</h4>
                        
                        <div class="stat-row">
                            <div class="stat-item">
                                <strong>Type 1:</strong> 
                                <span class="type-badge type-${selectedPokemon.type1.toLowerCase()}">${selectedPokemon.type1}</span>
                            </div>
                            <div class="stat-item">
                                <strong>Type 2:</strong> 
                                ${selectedPokemon.type2
                                    ? `<span class="type-badge type-${selectedPokemon.type2.toLowerCase()}">${selectedPokemon.type2}</span>`
                                    : "None"
                                }
                            </div>
                        </div>
                        
                        <div class="stat-row">
                            <div class="stat-item">
                                <strong>Height:</strong> ${selectedPokemon.height} m
                            </div>
                            <div class="stat-item">
                                <strong>Weight:</strong> ${selectedPokemon.weight} kg
                            </div>
                        </div>
                        
                        <div class="stat-row">
                            <div class="stat-item">
                                <strong>Base XP:</strong> ${selectedPokemon.base_experience}
                            </div>
                            <div class="stat-item">
                                <strong>Generation:</strong> ${selectedPokemon.generation}
                            </div>
                        </div>
                        
                        <div class="stat-row">
                            <div class="stat-item">
                                <strong>Legendary:</strong> ${legendaryStatus}
                            </div>
                        </div>
                    </div>
                    
                    <div class="stat-group">
                        <h4>Base Stats</h4>
                        
                        <div class="stat-bar-row">
                            <div class="stat-label">HP</div>
                            <div class="stat-value">${selectedPokemon.hp}</div>
                            <div class="stat-bar-container">
                                <div class="stat-bar">
                                    <div class="stat-fill hp-fill" style="width: ${Math.min(100, selectedPokemon.hp / 2)}%;"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="stat-bar-row">
                            <div class="stat-label">Attack</div>
                            <div class="stat-value">${selectedPokemon.attack}</div>
                            <div class="stat-bar-container">
                                <div class="stat-bar">
                                    <div class="stat-fill attack-fill" style="width: ${Math.min(100, selectedPokemon.attack / 2)}%;"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="stat-bar-row">
                            <div class="stat-label">Defense</div>
                            <div class="stat-value">${selectedPokemon.defense}</div>
                            <div class="stat-bar-container">
                                <div class="stat-bar">
                                    <div class="stat-fill defense-fill" style="width: ${Math.min(100, selectedPokemon.defense / 2)}%;"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="stat-bar-row">
                            <div class="stat-label">Sp. Atk</div>
                            <div class="stat-value">${selectedPokemon.sp_atk}</div>
                            <div class="stat-bar-container">
                                <div class="stat-bar">
                                    <div class="stat-fill spatk-fill" style="width: ${Math.min(100, selectedPokemon.sp_atk / 2)}%;"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="stat-bar-row">
                            <div class="stat-label">Sp. Def</div>
                            <div class="stat-value">${selectedPokemon.sp_def}</div>
                            <div class="stat-bar-container">
                                <div class="stat-bar">
                                    <div class="stat-fill spdef-fill" style="width: ${Math.min(100, selectedPokemon.sp_def / 2)}%;"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="stat-bar-row">
                            <div class="stat-label">Speed</div>
                            <div class="stat-value">${selectedPokemon.speed}</div>
                            <div class="stat-bar-container">
                                <div class="stat-bar">
                                    <div class="stat-fill speed-fill" style="width: ${Math.min(100, selectedPokemon.speed / 2)}%;"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
    // Add event listener to the battle button in details view
    document.getElementById('detail-battle-btn')?.addEventListener('click', () => {
      addPokemonToBattle(selectedPokemon);
    });
  }

  // Set up filter input events
  const filterInputs = document.querySelectorAll(".filter-input");

  filterInputs.forEach((input) => {
    input.addEventListener("change", function () {
      if (input.id === "filter-sort") {
        sortOption = input.value;
      } else {
        updateFilters();
      }
      applyFiltersAndSearch();
    });
  });

  // Range inputs
  const rangeInputs = document.querySelectorAll(".range-min, .range-max");
  rangeInputs.forEach((input) => {
    input.addEventListener("input", function () {
      updateFilters();
      applyFiltersAndSearch();
    });
  });

  // Battle functionality
  function addPokemonToBattle(pokemon) {
    // If both slots are filled, show a message and return
    if (battlePokemon1 && battlePokemon2) {
      alert("Both battle slots are already filled. Remove a Pokémon first.");
      return;
    }
    
    // If this Pokémon is already in a slot, do nothing
    if ((battlePokemon1 && battlePokemon1.id === pokemon.id) || 
        (battlePokemon2 && battlePokemon2.id === pokemon.id)) {
      alert(`${pokemon.name} is already selected for battle.`);
      return;
    }
    
    // Determine which slot to fill
    if (!battlePokemon1) {
      battlePokemon1 = pokemon;
      renderBattlePokemon(pokemon, pokemonSlot1, 1);
    } else {
      battlePokemon2 = pokemon;
      renderBattlePokemon(pokemon, pokemonSlot2, 2);
    }
    
    // Enable or disable the battle button based on whether both slots are filled
    battleBtn.disabled = !(battlePokemon1 && battlePokemon2);
    
    // Hide battle result when Pokemon selection changes
    battleResult.style.display = "none";
  }
  
  function renderBattlePokemon(pokemon, slot, position) {
    // Parse sprites if needed
    let sprites;
    if (typeof pokemon.sprites === "string") {
      try {
        sprites = JSON.parse(pokemon.sprites);
      } catch (e) {
        sprites = { normal: "", animated: "" };
      }
    } else {
      sprites = pokemon.sprites || { normal: "", animated: "" };
    }
    
    const spriteUrl = sprites.normal || "";
    
    // Create battle card HTML
    slot.classList.remove('empty-slot');
    slot.innerHTML = `
      <button class="remove-btn" data-position="${position}">×</button>
      <img src="${spriteUrl}" alt="${pokemon.name}">
      <h4>${pokemon.name}</h4>
      <div class="card-types">
        <span class="type-badge type-${pokemon.type1.toLowerCase()}">${pokemon.type1}</span>
        ${pokemon.type2 ? `<span class="type-badge type-${pokemon.type2.toLowerCase()}">${pokemon.type2}</span>` : ''}
      </div>
    `;
    
    // Add remove button event listener
    slot.querySelector('.remove-btn').addEventListener('click', (e) => {
      const position = parseInt(e.target.getAttribute('data-position'));
      removeBattlePokemon(position);
    });
  }
  
  function removeBattlePokemon(position) {
    if (position === 1) {
      battlePokemon1 = null;
      pokemonSlot1.classList.add('empty-slot');
      pokemonSlot1.innerHTML = '<div class="pokemon-placeholder">Select a Pokémon</div>';
    } else {
      battlePokemon2 = null;
      pokemonSlot2.classList.add('empty-slot');
      pokemonSlot2.innerHTML = '<div class="pokemon-placeholder">Select a Pokémon</div>';
    }
    
    // Disable battle button if either slot is empty
    battleBtn.disabled = !(battlePokemon1 && battlePokemon2);
    
    // Hide battle result when Pokemon selection changes
    battleResult.style.display = "none";
  }
  
  function startBattle() {
    if (!battlePokemon1 || !battlePokemon2) {
      alert("Please select two Pokémon for battle.");
      return;
    }
    
    // Show loading state
    battleBtn.disabled = true;
    battleBtn.textContent = "Battling...";
    
    // Prepare data for the battle prediction API
    const battleData = {
      pokemon1: battlePokemon1.name,
      pokemon2: battlePokemon2.name
    };
    
    // Call the battle prediction API
    fetch('/api/battle', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(battleData)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Battle prediction failed');
      }
      return response.json();
    })
    .then(result => {
      // Show battle result
      battleWinner.textContent = `Winner: ${result.winner}`;
      battleConfidence.textContent = `Confidence: ${result.probability}%`;
      battleResult.style.display = "block";
      
      // Reset button state
      battleBtn.disabled = false;
      battleBtn.textContent = "Start Battle!";
    })
    .catch(error => {
      console.error('Battle error:', error);
      alert('Battle prediction failed. Please try again.');
      
      // Reset button state
      battleBtn.disabled = false;
      battleBtn.textContent = "Start Battle!";
    });
  }

  function updateFilters() {
    currentFilters = {};

    // Extract standard filters
    const standardFilters = ["type1", "type2", "generation", "legendary"];
    standardFilters.forEach((filter) => {
      const input = document.getElementById(`filter-${filter}`);
      if (input && input.value.trim() !== "") {
        currentFilters[filter] = input.value.trim();
      }
    });

    // Extract range filters
    const rangeFilters = ["hp", "attack", "speed"];
    rangeFilters.forEach((filter) => {
      const minInput = document.getElementById(`filter-${filter}-min`);
      const maxInput = document.getElementById(`filter-${filter}-max`);

      if (minInput && minInput.value.trim() !== "") {
        currentFilters[`${filter}_min`] = parseInt(minInput.value.trim());
      }

      if (maxInput && maxInput.value.trim() !== "") {
        currentFilters[`${filter}_max`] = parseInt(maxInput.value.trim());
      }
    });

    renderActiveFilters();
  }

  function renderActiveFilters() {
    activeFiltersContainer.innerHTML = "";

    Object.entries(currentFilters).forEach(([key, value]) => {
      const filterTag = document.createElement("div");
      filterTag.className = "active-filter-tag";

      let displayName = key
        .replace("_", " ")
        .replace(/^\w/, (c) => c.toUpperCase());

      if (key === "type1") displayName = "Type 1";
      if (key === "type2") displayName = "Type 2";
      if (key === "hp_min") displayName = "Min HP";
      if (key === "hp_max") displayName = "Max HP";
      if (key === "attack_min") displayName = "Min Attack";
      if (key === "attack_max") displayName = "Max Attack";
      if (key === "speed_min") displayName = "Min Speed";
      if (key === "speed_max") displayName = "Max Speed";

      filterTag.innerHTML = `
        ${displayName}: ${value}
        <i class="fas fa-times" data-filter="${key}"></i>
      `;

      activeFiltersContainer.appendChild(filterTag);
    });

    // Add event listeners to remove buttons
    document.querySelectorAll(".active-filter-tag i").forEach((removeBtn) => {
      removeBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        const filterKey = this.getAttribute("data-filter");

        // Clear the corresponding input
        if (filterKey.includes("_min") || filterKey.includes("_max")) {
          const inputId = `filter-${filterKey}`;
          document.getElementById(inputId).value = "";
        } else {
          document.getElementById(`filter-${filterKey}`).value = "";
        }

        // Remove from current filters
        delete currentFilters[filterKey];
        renderActiveFilters();
        applyFiltersAndSearch();
      });
    });
  }

  function resetFilters() {
    // Reset all filter inputs
    filterInputs.forEach((input) => {
      input.value = "";
    });

    // Reset range inputs
    rangeInputs.forEach((input) => {
      input.value = "";
    });

    // Reset sort option
    document.getElementById("filter-sort").value = "id";
    sortOption = "id";

    // Clear current filters
    currentFilters = {};
    renderActiveFilters();

    // Apply reset
    searchBox.value = "";
    searchTerm = "";
    applyFiltersAndSearch();
  }

  function applyFiltersAndSearch() {
    const filteredPokemons = filterPokemons(allPokemons);
    renderPokemonList(filteredPokemons);
  }

  function filterPokemons(pokemons) {
    return pokemons.filter((pokemon) => {
      // Apply search
      if (searchTerm && !pokemon.name.toLowerCase().includes(searchTerm)) {
        return false;
      }

      // Apply standard filters
      for (const [key, value] of Object.entries(currentFilters)) {
        // Skip range filters
        if (key.includes("_min") || key.includes("_max")) continue;

        if (key === "legendary") {
          // Handle boolean values
          const boolValue = value === "true";
          if (pokemon[key] !== boolValue) return false;
        } else if (
          pokemon[key]?.toString().toLowerCase() !== value.toLowerCase()
        ) {
          return false;
        }
      }

      // Apply range filters
      const rangeFilters = {
        hp: ["hp_min", "hp_max"],
        attack: ["attack_min", "attack_max"],
        speed: ["speed_min", "speed_max"],
      };

      for (const [stat, [minKey, maxKey]] of Object.entries(rangeFilters)) {
        const min = currentFilters[minKey];
        const max = currentFilters[maxKey];

        if (min !== undefined && pokemon[stat] < min) return false;
        if (max !== undefined && pokemon[stat] > max) return false;
      }

      return true;
    });
  }
});
