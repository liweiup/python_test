# -*- coding: utf-8 -*-
import sys
import os
from app import create_app
from app.api.cms.model.group import Group
from app.api.cms.model.group_permission import GroupPermission
from app.api.cms.model.permission import Permission
from app.api.cms.model.user import User
from app.api.cms.model.user_group import UserGroup
from app.api.cms.model.user_identity import UserIdentity
from app.config.code_message import MESSAGE

try:
    app = create_app(
        group_model=Group,
        user_model=User,
        group_permission_model=GroupPermission,
        permission_model=Permission,
        identity_model=UserIdentity,
        user_group_model=UserGroup,
        config_MESSAGE=MESSAGE,
    )
    
    app.logger.info("Application created successfully")
    app.logger.info(f"Current working directory: {os.getcwd()}")
    app.logger.info(f"Python executable: {sys.executable}")
    
except Exception as e:
    print(f"Error creating app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


if app.config.get("ENV") != "production":

    @app.route("/")
    def slogan():
        return """
        <style type="text/css">
            * {
                padding: 0;
                margin: 0;
            }

            div {
                padding: 4px 48px;
            }

            a {
                color: black;
                cursor: pointer;
                text-decoration: none
            }

            a:hover {
                text-decoration: None;
            }

            body {
                background: #fff;
                font-family:
                    "Century Gothic", "Microsoft yahei";
                color: #333;
                font-size: 18px;
            }

            h1 {
                font-size: 100px;
                font-weight: normal;
                margin-bottom: 12px;
            }

            p {
                line-height: 1.6em;
                font-size: 42px
            }
        </style>
        <div style="padding: 24px 48px;">
            <p>
                <a href="https://www.talelin.com" target="_Blank">Lin</a>
                <br />
                <span style="font-size:30px">
                    <a href="/apidoc/redoc">心上无垢</a>，<a href="/apidoc/swagger">林间有风</a>。
                </span>
            </p>
        </div>
        """


if __name__ == "__main__":
    try:
        app.logger.info("Starting Flask development server...")
        app.logger.warning(
            """
            ----------------------------
            |  app.run() => flask run  |
            ----------------------------
            """
        )
        
        # 检查是否在打包环境中
        import sys
        if getattr(sys, 'frozen', False):
            # 打包环境，禁用reloader
            app.logger.info("Running in packaged environment, disabling reloader")
            app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
        else:
            # 开发环境，可以启用reloader
            app.logger.info("Running in development environment")
            app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
            
    except Exception as e:
        app.logger.error(f"Error starting server: {e}")
        import traceback
        app.logger.error(traceback.format_exc())
        print(f"Error starting server: {e}")
        traceback.print_exc()
        sys.exit(1)
