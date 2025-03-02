---
layout: page
title: projects
permalink: /projects/
description: 
nav: true
nav_order: 2
display_categories: [software, hardware]
horizontal: false
---

<!-- Project Introduction -->
<div class="project-intro">
  <p>This page showcases my journey through various projects. The timeline view presents projects chronologically with a central navigation bar, while the grid view organizes projects by organization. Navigate using arrow keys or WASD (↑/W and ↓/S to move between projects, ←/A and →/D to switch views). Click any project to view details in a modal window.</p>
</div>

<!-- View Switcher with same style as timeline filters -->
<div class="view-switcher-floating">
  <div class="switcher-container">
    <div class="switcher-slider"></div>
    <button class="switcher-btn active" data-view="timeline">Timeline</button>
    <button class="switcher-btn" data-view="grid">Grid</button>
  </div>
</div>

<!-- Timeline View -->
<div id="timeline-view" class="view-container">
  <div class="projects-timeline">
    {% include_relative projects_timeline_content.html %}
  </div>
</div>

<!-- Grid View -->
<div id="grid-view" class="view-container" style="display: none;">
  <div class="projects">
    <!-- Get all unique organizations -->
    {% assign all_projects = site.projects | sort: "date" | reverse %}
    {% assign organizations = "" | split: "" %}
    {% for project in all_projects %}
      {% if project.organization %}
        {% assign organizations = organizations | push: project.organization %}
      {% endif %}
    {% endfor %}
    
    <!-- Remove duplicates -->
    {% assign unique_organizations = organizations | uniq %}
    
    <!-- Manual organization order - reverse chronological -->
    {% assign org_order = "University of Wisconsin-Madison,NVIDIA,IIT Madras,High School" | split: "," %}
    
    <!-- Sort organizations in desired order -->
    {% assign sorted_orgs = "" | split: "" %}
    {% for desired_org in org_order %}
      {% for org in unique_organizations %}
        {% if org == desired_org %}
          {% assign sorted_orgs = sorted_orgs | push: org %}
          {% break %}
        {% endif %}
      {% endfor %}
    {% endfor %}
    
    <!-- Add any remaining organizations not in the predefined list -->
    {% for org in unique_organizations %}
      {% unless sorted_orgs contains org %}
        {% assign sorted_orgs = sorted_orgs | push: org %}
      {% endunless %}
    {% endfor %}
    
    {% assign unique_organizations = sorted_orgs %}
    
    <!-- Display projects by organization -->
    {% for org in unique_organizations %}
      <a id="{{ org | slugify }}" href=".#{{ org | slugify }}">
        <h2 class="category" {% for project in all_projects %}{% if project.organization == org and project.org_color %}style="color: {{ project.org_color }};"{% break %}{% endif %}{% endfor %}>{{ org }}</h2>
      </a>
      
      {% assign org_projects = all_projects | where: "organization", org %}
      
      <!-- Generate cards for each project -->
      {% if page.horizontal %}
        <div class="container">
          <div class="row row-cols-1 row-cols-md-2">
          {% for project in org_projects %}
            {% include projects_horizontal.liquid %}
          {% endfor %}
          </div>
        </div>
      {% else %}
        <div class="row row-cols-2 row-cols-md-4">
          {% for project in org_projects %}
            {% include projects.liquid %}
          {% endfor %}
        </div>
      {% endif %}
    {% endfor %}
    
    <!-- Projects without organization -->
    {% assign no_org_projects = all_projects | where_exp: "item", "item.organization == nil or item.organization == ''" %}
    {% if no_org_projects.size > 0 %}
      <a id="other" href=".#other">
        <h2 class="category">Other Projects</h2>
      </a>
      
      {% if page.horizontal %}
        <div class="container">
          <div class="row row-cols-1 row-cols-md-2">
          {% for project in no_org_projects %}
            {% include projects_horizontal.liquid %}
          {% endfor %}
          </div>
        </div>
      {% else %}
        <div class="row row-cols-2 row-cols-md-4">
          {% for project in no_org_projects %}
            {% include projects.liquid %}
          {% endfor %}
        </div>
      {% endif %}
    {% endif %}
  </div>
</div>

<!-- Project Modal Container -->
<div class="project-modal-backdrop" id="project-modal-backdrop" onclick="closeProjectModalFromBackdrop(event)">
  <div class="project-modal" id="project-modal">
    <div id="modal-content-container"></div>
  </div>
</div>


<!-- View Switcher Script -->
<script>
  // Project Modal Functions
  function openProjectModal(element) {
    const projectId = element.getAttribute('data-project-id');
    const modalContent = document.getElementById(`modal-content-${projectId}`);
    const modalContainer = document.getElementById('modal-content-container');
    const modal = document.getElementById('project-modal');
    const backdrop = document.getElementById('project-modal-backdrop');
    
    if (modalContent && modalContainer) {
      // Reset the scroll position of the modal
      if (modal) {
        modal.scrollTop = 0;
        
        // Also ensure scroll is reset after the animation starts
        setTimeout(() => {
          modal.scrollTop = 0;
        }, 10);
      }
      
      // Clone the content to the modal
      const contentHtml = modalContent.innerHTML;
      
      // Add close button to the header section in the HTML
      const headerRegex = /<div class="modal-header"([^>]*)>/;
      const headerWithCloseButton = '<div class="modal-header"$1><button class="modal-close" onclick="closeProjectModal()">×</button>';
      const modifiedContent = contentHtml.replace(headerRegex, headerWithCloseButton);
      
      // Add the HTML to the modal
      modalContainer.innerHTML = modifiedContent;
      
      // Show modal with animation
      backdrop.style.display = 'flex';
      setTimeout(() => {
        backdrop.classList.add('visible');
        modal.classList.add('visible');
      }, 10);
      
      // Prevent scrolling on the body
      document.body.style.overflow = 'hidden';
      
      // Handle escape key
      document.addEventListener('keydown', handleModalKeypress);
    }
  }
  
  function closeProjectModal() {
    const modal = document.getElementById('project-modal');
    const backdrop = document.getElementById('project-modal-backdrop');
    
    // Hide with animation
    modal.classList.remove('visible');
    backdrop.classList.remove('visible');
    
    // After animation completes, hide completely
    setTimeout(() => {
      backdrop.style.display = 'none';
      // Clear modal content
      document.getElementById('modal-content-container').innerHTML = '';
    }, 300);
    
    // Restore scrolling
    document.body.style.overflow = '';
    
    // Remove event listeners
    document.removeEventListener('keydown', handleModalKeypress);
  }
  
  function handleModalKeypress(e) {
    if (e.key === 'Escape') {
      closeProjectModal();
    }
  }
  
  function closeProjectModalFromBackdrop(event) {
    // Only close if clicking directly on the backdrop, not on the modal content
    if (event.target.id === 'project-modal-backdrop') {
      closeProjectModal();
    }
  }

  document.addEventListener('DOMContentLoaded', function() {
    const timelineView = document.getElementById('timeline-view');
    const gridView = document.getElementById('grid-view');
    const switcherBtns = document.querySelectorAll('.switcher-btn');
    const switcherSliders = document.querySelectorAll('.switcher-slider');
    
    // Current view and active project tracking
    let currentView = 'timeline';
    let currentProjectIndex = 0;
    let allProjects = [];
    
    // Initialize all switchers
    const activeBtnIndex = 0; // Timeline is active by default (index 0)
    
    // Position sliders under active buttons
    switcherSliders.forEach(slider => {
      const btnWidth = 100 / 2; // Always 2 buttons (timeline/grid)
      slider.style.left = `calc(${btnWidth * activeBtnIndex}% + 6px)`;
      slider.style.width = `calc(${btnWidth}% - 12px)`;
    });
    
    // Function to switch views
    function switchView(viewType) {
      // Only switch if it's a different view
      if (viewType !== currentView) {
        currentView = viewType;
        
        // Update all buttons with the same data-view attribute
        document.querySelectorAll(`.switcher-btn[data-view="${viewType}"]`).forEach(button => {
          const buttonContainer = button.closest('.switcher-container');
          const containerButtons = buttonContainer.querySelectorAll('.switcher-btn');
          const containerSlider = buttonContainer.querySelector('.switcher-slider');
          
          // Update active states in this container
          containerButtons.forEach(b => b.classList.remove('active'));
          button.classList.add('active');
          
          // Find the button's index within its own container
          const buttonIndex = Array.from(containerButtons).indexOf(button);
          
          // Move slider for this container
          const btnWidth = 100 / containerButtons.length;
          containerSlider.style.left = `calc(${btnWidth * buttonIndex}% + 6px)`;
          containerSlider.style.width = `calc(${btnWidth}% - 12px)`;
        });
        
        // Update view
        if (viewType === 'timeline') {
          timelineView.style.display = '';
          gridView.style.display = 'none';
          
          // Force re-layout and positioning
          if (window.dispatchEvent) {
            window.dispatchEvent(new Event('load'));
          }
        } else if (viewType === 'grid') {
          timelineView.style.display = 'none';
          gridView.style.display = '';
        }
      }
    }
    
    // Function to get all visible timeline projects
    function getVisibleTimelineProjects() {
      return Array.from(document.querySelectorAll('.timeline-entry')).filter(entry => 
        entry.style.display !== 'none'
      );
    }
    
    // Function to get all visible grid projects
    function getVisibleGridProjects() {
      return Array.from(document.querySelectorAll('#grid-view a[id]')).filter(entry => 
        window.getComputedStyle(entry).display !== 'none'
      );
    }
    
    // Function to navigate to a project by index
    function navigateToProject(index) {
      if (currentView === 'timeline') {
        allProjects = getVisibleTimelineProjects();
        
        // Don't wrap around - stop at boundaries
        if (index < 0) index = 0;
        if (index >= allProjects.length) index = allProjects.length - 1;
        
        if (allProjects.length > 0) {
          currentProjectIndex = index;
          const project = allProjects[index];
          
          // Always move to the next/previous project regardless of current scroll position
          const projectRect = project.getBoundingClientRect();
          const viewportHeight = window.innerHeight;
          
          // Find the dot for centering
          const dot = project.querySelector('.timeline-dot');
          if (dot) {
            const dotRect = dot.getBoundingClientRect();
            const visualOffset = -10;
            
            // Force exact positioning to the selected project
            const targetY = window.scrollY + dotRect.top - (viewportHeight / 2) + visualOffset;
            
            window.scrollTo({
              top: targetY,
              behavior: 'smooth'
            });
          } else {
            // Fallback to center the project itself
            const targetY = window.scrollY + projectRect.top + (projectRect.height / 2) - (viewportHeight / 2);
            window.scrollTo({
              top: targetY,
              behavior: 'smooth'
            });
          }
          
          // Highlight this project
          allProjects.forEach(p => p.classList.remove('active'));
          project.classList.add('active');
        }
      } else {
        allProjects = getVisibleGridProjects();
        
        // Don't wrap around - stop at boundaries
        if (index < 0) index = 0;
        if (index >= allProjects.length) index = allProjects.length - 1;
        
        if (allProjects.length > 0) {
          currentProjectIndex = index;
          const project = allProjects[index];
          
          // Force scroll to the exact project position
          project.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center'
          });
          
          // Add visual highlighting for grid view too
          const gridItems = document.querySelectorAll('#grid-view .card');
          gridItems.forEach(item => {
            item.style.transform = 'scale(1)';
            item.style.boxShadow = '';
          });
          
          const targetCard = project.querySelector('.card');
          if (targetCard) {
            targetCard.style.transform = 'scale(1.02)';
            targetCard.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.15)';
          }
        }
      }
    }
    
    // Track current active project on scroll for timeline view
    window.addEventListener('scroll', function() {
      if (currentView === 'timeline') {
        const viewportHeight = window.innerHeight;
        const viewportCenter = viewportHeight / 2;
        const visibleProjects = getVisibleTimelineProjects();
        
        let closestProject = null;
        let closestDistance = Infinity;
        let closestIndex = 0;
        
        visibleProjects.forEach((project, index) => {
          const rect = project.getBoundingClientRect();
          const entryCenter = rect.top + (rect.height / 2);
          const distance = Math.abs(viewportCenter - entryCenter);
          
          if (distance < closestDistance) {
            closestDistance = distance;
            closestProject = project;
            closestIndex = index;
          }
        });
        
        if (closestProject) {
          currentProjectIndex = closestIndex;
        }
      }
    });
    
    // Initialize project tracking on page load
    setTimeout(() => {
      // Get initial lists of projects
      if (currentView === 'timeline') {
        allProjects = getVisibleTimelineProjects();
      } else {
        allProjects = getVisibleGridProjects();
      }
      
      // Start with the first project selected in timeline view
      if (allProjects.length > 0 && currentView === 'timeline') {
        navigateToProject(0);
      }
    }, 500); // Small delay to ensure page is rendered
    
    // Set up keyboard navigation
    document.addEventListener('keydown', function(e) {
      const key = e.key.toLowerCase();
      
      // Check if modal is open - if so, only handle Escape key
      const modalBackdrop = document.getElementById('project-modal-backdrop');
      if (modalBackdrop && modalBackdrop.style.display === 'flex') {
        return; // Let the modal's own keyboard handler take care of it
      }
      
      // Prevent default arrow key scrolling
      if (['arrowup', 'arrowdown', 'arrowleft', 'arrowright', 'w', 'a', 's', 'd'].includes(key)) {
        e.preventDefault();
      }
      
      // Switch views with left/right arrow or A/D keys
      if (key === 'arrowleft' || key === 'a') {
        switchView('timeline');
        // After switching to timeline, select first project
        setTimeout(() => navigateToProject(0), 300);
      } else if (key === 'arrowright' || key === 'd') {
        switchView('grid');
        // After switching to grid, select first project
        setTimeout(() => navigateToProject(0), 300);
      }
      
      // Navigate between projects with up/down arrow or W/S keys
      if (key === 'arrowup' || key === 'w') {
        navigateToProject(currentProjectIndex - 1);
      } else if (key === 'arrowdown' || key === 's') {
        navigateToProject(currentProjectIndex + 1);
      }
      
      // Open the current active project with Enter key
      if (key === 'enter') {
        if (currentView === 'timeline') {
          allProjects = getVisibleTimelineProjects();
          if (allProjects.length > 0 && currentProjectIndex >= 0 && currentProjectIndex < allProjects.length) {
            const activeProject = allProjects[currentProjectIndex];
            if (activeProject) {
              openProjectModal(activeProject.querySelector('.timeline-card-link'));
            }
          }
        } else {
          allProjects = getVisibleGridProjects();
          if (allProjects.length > 0 && currentProjectIndex >= 0 && currentProjectIndex < allProjects.length) {
            const activeProject = allProjects[currentProjectIndex];
            if (activeProject) {
              openProjectModal(activeProject);
            }
          }
        }
      }
    });
    
    // Set up switcher buttons
    switcherBtns.forEach((btn, index) => {
      btn.addEventListener('click', function() {
        const viewType = this.getAttribute('data-view');
        switchView(viewType);
      });
    });
  });
</script>
