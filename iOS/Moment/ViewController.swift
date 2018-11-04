//
//  ViewController.swift
//  Moment
//
//  Created by Jessie Mindel on 11/3/18.
//  Copyright © 2018 jmindel. All rights reserved.
//

import UIKit
import SceneKit
import ARKit

class ViewController: UIViewController, ARSCNViewDelegate {

    @IBOutlet var sceneView: ARSCNView!
    
    @IBOutlet var createHubButton: UIButton!
    @IBOutlet var createStickyButton: UIButton!
    @IBOutlet var exitStickyButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Set the view's delegate
        sceneView.delegate = self
        
        // Show statistics such as fps and timing information
        sceneView.showsStatistics = true
        
        // Create a new scene
        let scene = SCNScene(named: "art.scnassets/ship.scn")!
        
        // Set the scene to the view
        sceneView.scene = scene
        
        // Handle debug buttons
        createHubButton.isHidden = false
        createStickyButton.isHidden = true
        exitStickyButton.isHidden = true
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        // Create a session configuration
        let configuration = ARWorldTrackingConfiguration()
        configuration.planeDetection = [.horizontal, .vertical]

        // Run the view's session
        sceneView.session.run(configuration)
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        
        // Pause the view's session
        sceneView.session.pause()
    }
    
    func session(_ session: ARSession, didFailWithError error: Error) {
        // Present an error message to the user
        
    }
    
    func sessionWasInterrupted(_ session: ARSession) {
        // Inform the user that the session has been interrupted, for example, by presenting an overlay
        
    }
    
    func sessionInterruptionEnded(_ session: ARSession) {
        // Reset tracking and/or remove existing anchors if consistent tracking is required
        
    }
    
    @IBAction func hubButtonTouch(_ sender: Any) {
        // Handle button hiding
        createHubButton.isHidden = true
        createStickyButton.isHidden = false
        exitStickyButton.isHidden = false
        
        // FIXME: This needs anchoring! It kind of just floats around weirdly!
        let hubDot = SCNNode(geometry: SCNSphere(radius: 0.2)) // Temporarily creates dot at the core of the hub for debugging purposes
        let camera = sceneView.session.currentFrame!.camera
        let cameraNode = SCNNode()
        cameraNode.transform = SCNMatrix4(camera.transform)
        let position = SCNVector3(x: 0, y: 0, z: -1)
        updatePositionAndOrientationOf(hubDot, withPosition: position, relativeTo: cameraNode)
        sceneView.scene.rootNode.addChildNode(hubDot)
    }
    
    @IBAction func stickyButtonTouch(_ sender: Any) {
        
    }
    
    @IBAction func stickyExitButtonTouch(_ sender: Any) {
        // Handle button hiding
        createHubButton.isHidden = false
        createStickyButton.isHidden = true
        exitStickyButton.isHidden = true
        
        //let sticky = Sticky()
        //updatePositionAndOrientationOf(sticky, withPosition: <#T##SCNVector3#>, relativeTo: <#T##SCNNode#>)
    }
    
    // Courtesy of https://stackoverflow.com/questions/42029347/position-a-scenekit-object-in-front-of-scncameras-current-orientation/42030679
    func updatePositionAndOrientationOf(_ node: SCNNode, withPosition position: SCNVector3, relativeTo referenceNode: SCNNode) {
        let referenceNodeTransform = matrix_float4x4(referenceNode.transform)
        
        // Setup a translation matrix with the desired position
        var translationMatrix = matrix_identity_float4x4
        translationMatrix.columns.3.x = position.x
        translationMatrix.columns.3.y = position.y
        translationMatrix.columns.3.z = position.z
        
        // Combine the configured translation matrix with the referenceNode's transform to get the desired position AND orientation
        let updatedTransform = matrix_multiply(referenceNodeTransform, translationMatrix)
        node.transform = SCNMatrix4(updatedTransform)
    }
    
    func getHubsIn(radius: Int) {
        
    }
}
