#!/usr/bin/env python3
"""
LRDEnE Guardian Slack Integration
================================

Copyright (c) 2026 LRDEnE. All rights reserved.

Real-time AI safety monitoring for Slack messages and content.
"""

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional

import requests
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_sdk.web.async_client import AsyncWebClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LRDEnEGuardianSlack:
    """LRDEnE Guardian Slack Integration"""
    
    def __init__(self):
        self.api_endpoint = os.getenv('LRDEN_GUARDIAN_API_ENDPOINT', 'http://localhost:5001')
        self.slack_bot_token = os.getenv('SLACK_BOT_TOKEN')
        self.slack_app_token = os.getenv('SLACK_APP_TOKEN')
        
        if not self.slack_bot_token or not self.slack_app_token:
            raise ValueError("SLACK_BOT_TOKEN and SLACK_APP_TOKEN environment variables are required")
        
        # Initialize Slack app
        self.app = AsyncApp(token=self.slack_bot_token)
        self.web_client = AsyncWebClient(token=self.slack_bot_token)
        
        # Configure app handlers
        self.setup_handlers()
        
        # Analysis cache
        self.analysis_cache = {}
        
    def setup_handlers(self):
        """Setup Slack event handlers"""
        
        @self.app.message()
        async def handle_message(event, say, client):
            """Handle incoming messages"""
            try:
                # Skip bot messages and messages with subtypes
                if event.get('bot_id') or event.get('subtype'):
                    return
                
                text = event.get('text', '')
                user_id = event.get('user')
                channel_id = event.get('channel')
                timestamp = event.get('ts')
                
                if not text or len(text.strip()) < 10:
                    return
                
                # Analyze the message
                analysis = await self.analyze_content(text, {
                    'source': 'slack_integration',
                    'user_id': user_id,
                    'channel_id': channel_id,
                    'timestamp': timestamp,
                    'message_type': 'message'
                })
                
                if analysis and not analysis.get('is_safe', True):
                    await self.handle_risky_content(analysis, event, say)
                    
            except Exception as e:
                logger.error(f"Error handling message: {e}")
        
        @self.app.command("/guardian-analyze")
        async def handle_analyze_command(ack, respond, command):
            """Handle manual analyze command"""
            await ack()
            
            try:
                text = command.get('text', '')
                if not text:
                    await respond("Please provide text to analyze. Usage: `/guardian-analyze <text>`")
                    return
                
                analysis = await self.analyze_content(text, {
                    'source': 'slack_command',
                    'user_id': command['user_id'],
                    'channel_id': command['channel_id'],
                    'command': True
                })
                
                if analysis:
                    await self.send_analysis_response(analysis, respond)
                else:
                    await respond("❌ Analysis failed. Please try again later.")
                    
            except Exception as e:
                logger.error(f"Error in analyze command: {e}")
                await respond("❌ An error occurred during analysis.")
        
        @self.app.command("/guardian-status")
        async def handle_status_command(ack, respond):
            """Handle status command"""
            await ack()
            
            try:
                status = await self.check_guardian_status()
                if status:
                    await respond(f"🛡️ LRDEnE Guardian Status: ✅ Online\nAPI Endpoint: `{self.api_endpoint}`")
                else:
                    await respond(f"🛡️ LRDEnE Guardian Status: ❌ Offline\nAPI Endpoint: `{self.api_endpoint}`")
                    
            except Exception as e:
                logger.error(f"Error in status command: {e}")
                await respond("❌ Unable to check status.")
        
        @self.app.command("/guardian-settings")
        async def handle_settings_command(ack, respond, command):
            """Handle settings command"""
            await ack()
            
            try:
                # Show current settings
                settings_text = f"""🛡️ LRDEnE Guardian Settings:
🔗 API Endpoint: `{self.api_endpoint}`
📊 Auto-analysis: Enabled
⚠️ Risk alerts: Enabled
📈 Statistics: Enabled

Use `/guardian-analyze <text>` to manually analyze content."""
                
                await respond(settings_text)
                
            except Exception as e:
                logger.error(f"Error in settings command: {e}")
                await respond("❌ Unable to retrieve settings.")
        
        @self.app.action("guardian_ignore")
        async def handle_ignore_action(ack, body, respond):
            """Handle ignore action"""
            await ack()
            
            try:
                # Log the ignore action
                original_message = body.get('original_message', {})
                await respond("⚠️ Content marked as ignored. Be cautious with this content.")
                
            except Exception as e:
                logger.error(f"Error handling ignore action: {e}")
        
        @self.app.action("guardian_review")
        async def handle_review_action(ack, body, respond):
            """Handle review action"""
            await ack()
            
            try:
                # Send detailed analysis
                original_message = body.get('original_message', {})
                analysis_id = original_message.get('analysis_id')
                
                if analysis_id and analysis_id in self.analysis_cache:
                    analysis = self.analysis_cache[analysis_id]
                    await self.send_detailed_analysis(analysis, respond)
                else:
                    await respond("❌ Analysis details not found.")
                    
            except Exception as e:
                logger.error(f"Error handling review action: {e}")
    
    async def analyze_content(self, content: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze content using LRDEnE Guardian API"""
        try:
            # Check cache first
            cache_key = hash(content + str(context))
            if cache_key in self.analysis_cache:
                return self.analysis_cache[cache_key]
            
            # Call LRDEnE Guardian API
            response = requests.post(
                f"{self.api_endpoint}/analyze",
                json={
                    "content": content,
                    "context": {
                        **context,
                        "timestamp": datetime.now().isoformat()
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                analysis = response.json()
                
                # Cache the result
                self.analysis_cache[cache_key] = analysis
                
                # Limit cache size
                if len(self.analysis_cache) > 1000:
                    oldest_key = next(iter(self.analysis_cache))
                    del self.analysis_cache[oldest_key]
                
                return analysis
            else:
                logger.error(f"API request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error analyzing content: {e}")
            return None
    
    async def handle_risky_content(self, analysis: Dict[str, Any], event: Dict[str, Any], say):
        """Handle risky content detection"""
        try:
            # Create analysis ID for this analysis
            analysis_id = f"{event['channel']}_{event['ts']}"
            self.analysis_cache[analysis_id] = analysis
            
            # Format risk message
            risk_level = analysis.get('risk_level', 'unknown')
            guardian_score = analysis.get('guardian_score', 0)
            issues = analysis.get('detected_issues', [])
            
            # Create warning message
            warning_blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"🛡️ *LRDEnE Guardian Alert*\n⚠️ *Risk Level: {risk_level.upper()}*\n📊 *Guardian Score: {guardian_score:.3f}*"
                    }
                }
            ]
            
            # Add issues if any
            if issues:
                issues_text = "\n".join([f"• {issue}" for issue in issues[:3]])
                warning_blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Detected Issues:*\n{issues_text}"
                    }
                })
            
            # Add action buttons
            warning_blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "📋 View Details"
                        },
                        "action_id": "guardian_review",
                        "value": analysis_id
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "⚠️ Ignore"
                        },
                        "action_id": "guardian_ignore",
                        "style": "danger"
                    }
                ]
            })
            
            # Send warning as ephemeral message to the user who posted
            await say(
                blocks=warning_blocks,
                user=event['user'],
                text="🛡️ LRDEnE Guardian: Risk detected in message"
            )
            
        except Exception as e:
            logger.error(f"Error handling risky content: {e}")
    
    async def send_analysis_response(self, analysis: Dict[str, Any], respond):
        """Send analysis response to user"""
        try:
            is_safe = analysis.get('is_safe', True)
            risk_level = analysis.get('risk_level', 'unknown')
            guardian_score = analysis.get('guardian_score', 0)
            confidence = analysis.get('confidence_score', 0)
            issues = analysis.get('detected_issues', [])
            recommendations = analysis.get('recommendations', [])
            
            # Create response blocks
            status_icon = "✅" if is_safe else "⚠️"
            status_text = "Safe Content" if is_safe else "Requires Review"
            
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"🛡️ *LRDEnE Guardian Analysis*\n{status_icon} *Status: {status_text}*\n📊 *Guardian Score: {guardian_score:.3f}*\n🎯 *Confidence: {confidence:.1%}*\n🔥 *Risk Level: {risk_level.upper()}*"
                    }
                }
            ]
            
            # Add issues if any
            if issues:
                issues_text = "\n".join([f"• {issue}" for issue in issues[:3]])
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*⚠️ Detected Issues:*\n{issues_text}"
                    }
                })
            
            # Add recommendations if any
            if recommendations:
                rec_text = "\n".join([f"• {rec}" for rec in recommendations[:3]])
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*💡 Recommendations:*\n{rec_text}"
                    }
                })
            
            await respond(blocks=blocks, text="🛡️ LRDEnE Guardian Analysis Complete")
            
        except Exception as e:
            logger.error(f"Error sending analysis response: {e}")
            await respond("❌ Error sending analysis results.")
    
    async def send_detailed_analysis(self, analysis: Dict[str, Any], respond):
        """Send detailed analysis information"""
        try:
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"🛡️ *LRDEnE Guardian - Detailed Analysis*\n\n" +
                        f"*Status:* {'✅ Safe' if analysis.get('is_safe') else '⚠️ Requires Review'}\n" +
                        f"*Guardian Score:* {analysis.get('guardian_score', 0):.3f}\n" +
                        f"*Confidence:* {analysis.get('confidence_score', 0):.1%}\n" +
                        f"*Risk Level:* {analysis.get('risk_level', 'unknown').upper()}\n" +
                        f"*Analysis Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                }
            ]
            
            # Add detailed issues
            issues = analysis.get('detected_issues', [])
            if issues:
                issues_text = "\n".join([f"• {issue}" for issue in issues])
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*🚨 All Detected Issues:*\n{issues_text}"
                    }
                })
            
            # Add detailed recommendations
            recommendations = analysis.get('recommendations', [])
            if recommendations:
                rec_text = "\n".join([f"• {rec}" for rec in recommendations])
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*💡 All Recommendations:*\n{rec_text}"
                    }
                })
            
            await respond(blocks=blocks, text="🛡️ LRDEnE Guardian - Detailed Analysis")
            
        except Exception as e:
            logger.error(f"Error sending detailed analysis: {e}")
            await respond("❌ Error retrieving detailed analysis.")
    
    async def check_guardian_status(self) -> bool:
        """Check if LRDEnE Guardian API is accessible"""
        try:
            response = requests.get(f"{self.api_endpoint}/api-info", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    async def start(self):
        """Start the Slack bot"""
        try:
            # Check Guardian API status
            if not await self.check_guardian_status():
                logger.warning("LRDEnE Guardian API is not accessible")
            
            # Start the app
            handler = AsyncSocketModeHandler(self.app, self.slack_app_token)
            await handler.start()
            
        except Exception as e:
            logger.error(f"Error starting Slack bot: {e}")
            raise

def main():
    """Main entry point"""
    try:
        bot = LRDEnEGuardianSlack()
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("Shutting down LRDEnE Guardian Slack bot...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
