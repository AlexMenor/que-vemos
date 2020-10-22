git diff --name-only HEAD^ HEAD | grep -E "(Dockerfile|pyproject.toml)"
  if [[ $? ]]; then
	      echo "::set-output name=run_docker_build::true"
		    else
			        echo "::set-output name=run_docker_build::false"
				  fi
