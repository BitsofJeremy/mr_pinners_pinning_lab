# pinning_lab/lab/views.py

# external imports
from flask import Blueprint, render_template, request, \
    redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required

# Local imports
from pinning_lab.database.models import Images, Users
from pinning_lab import db
from pinning_lab.utils.ipfs_utils import create_ipfs, \
    pin_ipfs, remove_ipfs, check_ipfs

# Logging
import logging
logger = logging.getLogger(__name__)

lab = Blueprint('lab', __name__)
lab.config = {}


@lab.record
def record_params(setup_state):
  app = setup_state.app
  lab.config = dict([(key, value) for (key, value) in app.config.items()])


def allowed_file(filename):
    """ Check file extension for required type """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in lab.config['ALLOWED_EXTENSIONS']


@lab.route('/pin_it', methods=['GET'])
def pin_it():
    """ pin GET page """
    return render_template('lab/pin_it.html')


@lab.route('/pin_it', methods=['POST'])
def pin_it_post():
    """ pin POST page """
    # TODO verify user has slots to pin
    name = request.form.get('name')
    description = request.form.get('description')
    # Check to make sure they put a file in the request
    if 'file' not in request.files:
        flash('YO! No file!')
        return redirect(request.url)
    file = request.files['file']
    # Again make sure there is a file
    if file.filename == '':
        flash('Hey There, No image selected for uploading')
        return redirect(request.url)
    # Name check
    # TODO maybe check for IPFS also?
    image_exists = Images.query.filter_by(name=name).first()
    if image_exists:
        flash('Image already exists, please try again')
        return redirect(url_for('lab.current_pins'))
    # User who dis?
    user_id = current_user.id

    if file and allowed_file(file.filename):
        # Verify they are legit not hacking the server
        # TODO try uploading the filename
        filename = secure_filename(file.filename)
        # upload file to Blockfrost
        # TODO celery ?
        res = create_ipfs(file)
        print(res)
        ipfs_hash = res['ipfs_hash']
        # OK now pin it
        # TODO celery ?
        pinned = pin_ipfs(ipfs_hash=ipfs_hash)
        if pinned:
            # Lets our info add to the DB
            new_image = Images(
                name=name,
                description=description,
                user_id=user_id,
                ipfs_hash=ipfs_hash,
                pinned=pinned
            )
            db.session.add(new_image)
            db.session.commit()
            flash("Pinned it.")
            logger.info("Pinned an image")
            return redirect(url_for('lab.current_pins'))
        else:
            logger.error('Pinning failed, sorry.')
            flash('Pinning failed, sorry.')
            return redirect(request.url)
    else:
        logger.error("mimetype check failed")
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@lab.route('/re_pin_it', methods=['GET'])
def re_pin_it():
    """ pin GET page """
    return render_template('lab/re_pin_it.html')


@lab.route('/re_pin_it', methods=['POST'])
def re_pin_it_post():
    """ Re-pin an image POST page """
    # TODO verify user has slots to pin
    name = request.form.get('name')
    description = request.form.get('description')
    ipfs_hash = request.form.get('ipfs_hash')
    # Should probably verify IPFS hash also
    hash_exists = Images.query.filter_by(ipfs_hash=ipfs_hash).first()
    if hash_exists:
        flash('IPFS hash already exists, please delete the other pinned image')
        return redirect(url_for('lab.current_pins'))
    user_id = current_user.id
    # TODO celery ?
    pinned = pin_it(ipfs_hash=ipfs_hash)
    if pinned:
        new_image = Images(
            name=name,
            description=description,
            user_id=user_id,
            ipfs_hash=ipfs_hash,
            pinned=pinned
        )
        db.session.add(new_image)
        db.session.commit()
        logger.info("User re-pinned an image")
        flash("Re-Pinned it.")
        return redirect(url_for('lab.current_pins'))
    else:
        logger.error('Re-Pinning failed, sorry.')
        flash('Re-Pinning failed, sorry.')
        return redirect(request.url)


@lab.route('/current_pins', methods=['GET'])
def current_pins():
    """ view page
    shows previously created user Images"""
    user = Users.query.filter_by(username=current_user.username).first()
    images = user.images
    return render_template(
        'lab/current_pins.html',
        username=current_user.username,
        images=images
    )


@login_required
@lab.route('/delete_pin/<int:image_id>', methods=['GET'])
def delete_pin(image_id):
    """ Delete Pin """
    # Get the hash from the DB
    image_data = Images.query.filter_by(id=image_id).first()
    ipfs_hash = image_data.ipfs_hash
    # TODO celery ?
    removed_pin = remove_ipfs(ipfs_hash=ipfs_hash)
    if removed_pin:
        logger.info(f"{current_user.username} tried to delete pin {image_id}")
        try:
            num_rows_deleted = Images.query.filter_by(id=image_id).delete()
            db.session.commit()
            logger.info(f"num_rows_deleted: {num_rows_deleted}")
            flash("Deleted Pin.")
        except:
            db.session.rollback()
            flash("Oops, something went wrong.")
        return redirect(url_for('lab.current_pins'))
    else:
        logger.error('Removing Pinning failed, sorry.')
        flash('Removing Pinning failed, sorry.')
        return redirect(request.url)
