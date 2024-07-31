# Clash of Clans -> Electro Dragon Placer

## Image Demonstration

<div style="display: flex; justify-content: space-between;">
  <div style="flex: 1; text-align: center;">
    <h3>Before</h3>
    <img src="assets/Before.png" alt="Before Image" style="max-width: 100%;">
  </div>
  <div style="flex: 1; text-align: center;">
    <h3>Uploading</h3>
    <img src="assets/UI.png" alt="Uploading Image" style="max-width: 100%;">
  </div>
  <div style="flex: 1; text-align: center;">
    <h3>After</h3>
    <img src="assets/After.png" alt="After Image" style="max-width: 100%;">
  </div>
</div>

## Description

The Clash of Clans -> Electro Dragon Placer is a tool designed to optimize the placement of Electro Dragons, a troop with a chaining attack in the game Clash of Clans. It analyzes the layout of enemy bases and suggests the best positions to deploy Electro Dragons for maximum effectiveness.

## Features

- Flask-based UI for receiving an input Clash of Clans base and outputting a new image with the overlaid positions of the electro dragons.
- JSON data of coordinates of Clash of Clans buildings in a base can be accessed in the `Model` class which uses RoboFlow3.0.
- Easier visualization of a 44x44 pixel depiction of the base along with all the building chains can be accessed in the `Buildings` class.